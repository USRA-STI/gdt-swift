# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT
# WITH UNLIMITED RIGHTS
#
# Grant No.: 80NSSC21K0651
# Grantee Name: Universities Space Research Association
# Grantee Address: 425 3rd Street SW, Suite 950, Washington DC 20024
#
# Copyright 2024 by Universities Space Research Association (USRA). All rights
# reserved.
#
# Developed by: Corinne Fletcher
#               Universities Space Research Association
#               Science and Technology Institute
#               https://sti.usra.edu
#
# This work is a derivative of the Gamma-ray Data Tools (GDT), including the
# Core and Fermi packages, originally developed by the following:
#
#     William Cleveland and Adam Goldstein
#     Universities Space Research Association
#     Science and Technology Institute
#     https://sti.usra.edu
#
#     Daniel Kocevski
#     National Aeronautics and Space Administration (NASA)
#     Marshall Space Flight Center
#     Astrophysics Branch (ST-12)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import numpy as np
import astropy.io.fits as fits

from gdt.core.phaii import Phaii
from gdt.core.data_primitives import Ebounds, Gti, TimeEnergyBins
from .headers import LightcurveHeaders
from ..time import Time

__all__ = ['BatLightcurve']


class BatLightcurve(Phaii):
    """PHAII class for GBM time history spectra.
    """


    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a BAT lightcurve FITS file and return the BatLightcurve object

        Args:
            file_path (str): The file path of the FITS file

        Returns:
            (:class:`GbmPhaii`)
        """
        obj = super().open(file_path, **kwargs)
        trigtime = None

        # get the headers
        hdrs = [hdu.header for hdu in obj.hdulist]
        if 'TRIGTIME' in hdrs[0].keys():
            headers = LightcurveHeaders.from_headers(hdrs)
            trigtime = float(headers['PRIMARY']['TRIGTIME'])
        else:
            headers = LightcurveHeaders.from_headers(hdrs)

        # the channel energy bounds
        ebounds = Ebounds.from_bounds(obj.column(2, 'E_MIN'),
                                      obj.column(2, 'E_MAX'))

        # the 2D time-channel counts data
        time = obj.column(1, 'TIME')
        #print(time.min, time.max)
        endtime = []
        for i in range(0,len(time)-1):
            endtime += [time[i+1]]
        endtime +=[hdrs[1]['TSTART']]
        exposure = obj._assert_exposure(obj.column(1, 'FRACEXP'))
        # if trigtime is not None:
        #     time -= trigtime
        #     endtime -= trigtime

        data = TimeEnergyBins(obj.column(1, 'TOTCOUNTS'), time, endtime, exposure,
                              obj.column(2, 'E_MIN'), obj.column(2, 'E_MAX'),
                              )

        # the good time intervals
        gti_start = obj.column(3, 'START')
        gti_stop = obj.column(3, 'STOP')
        if trigtime is not None:
            gti_start -= trigtime
            gti_stop -= trigtime
        gti = Gti.from_bounds(gti_start, gti_stop)

        class_ = cls

        obj.close()

        return class_.from_data(data, gti=gti, trigger_time=trigtime,
                                filename=obj.filename, headers=headers)

    def _build_hdulist(self):

        # create FITS and primary header
        hdulist = fits.HDUList()
        primary_hdu = fits.PrimaryHDU(header=self.headers['PRIMARY'])
        for key, val in self.headers['PRIMARY'].items():
            primary_hdu.header[key] = val
        hdulist.append(primary_hdu)

        # the spectrum extension
        rates_hdu = self._rates_table()
        hdulist.append(rates_hdu)


        # the ebounds extension
        ebounds_hdu = self._ebounds_table()
        hdulist.append(ebounds_hdu)


        # the GTI extension
        gti_hdu = self._gti_table()
        hdulist.append(gti_hdu)

        return hdulist

    def _build_headers(self, trigtime, tstart, tstop, num_chans):

        headers = self.headers.copy()
        for hdu in headers:
            hdu['TSTART'] = tstart
            hdu['TSTOP'] = tstop
            try:
                hdu['DETCHANS'] = num_chans
            except:
                pass
            if trigtime is not None:
                hdu['TRIGTIME'] = trigtime

        return headers

    def _ebounds_table(self):
        chan_col = fits.Column(name='CHANNEL', format='1I',
                               array=np.arange(self.num_chans, dtype=int))
        emin_col = fits.Column(name='E_MIN', format='1E', unit='keV',
                               array=self.ebounds.low_edges())
        emax_col = fits.Column(name='E_MAX', format='1E', unit='keV',
                               array=self.ebounds.high_edges())

        hdu = fits.BinTableHDU.from_columns([chan_col, emin_col, emax_col],
                                            header=self.headers['EBOUNDS'])
        for key, val in self.headers['EBOUNDS'].items():
            hdu.header[key] = val

        return hdu

    def _rates_table(self):
        tstart = np.copy(self.data.tstart)
        tstop = np.copy(self.data.tstop)
        if self.trigtime is not None:
            tstart += self.trigtime
            tstop += self.trigtime
        print(dir(self.data))
        time_col = fits.Column(name='TIME', format='1D', unit='s', array=tstart)
        print(time_col)
        counts_col = fits.Column(name='RATE',
                                 format='4D',
                                 bzero=32768, bscale=1, unit='count/s',
                                 array=self.data.rates)
        error_col = fits.Column(name='ERROR', format='4D', unit='count/s',
                                 bzero=32768, bscale=1, array=self.data.ratesuncertainty)
        totcounts_col = fits.Column(name='TOTCOUNTS', format='J', unit='counts',
                               array=self.data.counts)
        expos_col = fits.Column(name='FRACEXP', format='D',
                                array=self.data.exposure)

        hdu = fits.BinTableHDU.from_columns([time_col, rates_col, error_col, totcounts_col,
                                             expos_col], header=self.headers['RATE'])

        for key, val in self.headers['RATE'].items():
            hdu.header[key] = val

        return hdu

    def _gti_table(self):
        tstart = np.array(self.gti.low_edges())
        tstop = np.array(self.gti.high_edges())
        if self.trigtime is not None:
            tstart += self.trigtime
            tstop += self.trigtime

        start_col = fits.Column(name='START', format='1D', unit='s',
                                bzero=self.trigtime, array=tstart)
        stop_col = fits.Column(name='STOP', format='1D', unit='s',
                                bzero=self.trigtime, array=tstop)
        hdu = fits.BinTableHDU.from_columns([start_col, stop_col],
                                            header=self.headers['GTI'])

        for key, val in self.headers['GTI'].items():
            hdu.header[key] = val
        hdu.header.comments['TZERO1'] = 'Offset, equal to TRIGTIME'
        hdu.header.comments['TZERO2'] = 'Offset, equal to TRIGTIME'
        return hdu
