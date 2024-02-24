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
#
import numpy as np
import astropy.io.fits as fits

from gdt.core.pha import Pha
from gdt.core.data_primitives import Ebounds, Gti, EnergyBins
from gdt.core.file import FitsFileContextManager
from .headers import PhaHeaders
from ..time import Time

__all__ = ['BatPha']


class BatPha(Pha):
    def __init__(self):
        super().__init__()
    """PHA class for BAT spectra.
    """

    @classmethod
    def from_data(cls, data, gti=None, trigger_time=None, filename=None,
                  headers=None, channel_mask=None, header_type=PhaHeaders,
                  **kwargs):
        """Create a PHA object from an
        :class:`~.data_primitives.EnergyBins` object.

        Args:
            data (:class:`~.data_primitives.EnergyBins`):
                 The PHA count spectrum data
            gti (:class:`~.data_primitives.Gti`), optional):
                The good time intervals of the pectrum data.  If omitted, then
                assumes the range (0, exposure).
            trigger_time (float, optional): The trigger time, if applicable.
                                            If provided, the data times will be
                                            shifted relative to the trigger time.
                                            Default is zero.
            headers (:class:`~.headers.FileHeaders`): The file headers
            channel_mask (np.array(dtype=bool)):
                A boolean array representing the valid channels. If omitted,
                assumes all non-zero count channels are valid.
            header_type (:class:`~.headers.FileHeaders`):
                Default file header class. Only used if ``headers`` is not
                defined

        Returns:
            (:class:`Pha`)
        """
        obj = cls()
        obj._filename = filename

        # set data and ebounds
        if not isinstance(data, EnergyBins):
            raise TypeError('data must be of type EnergyBins')
        obj._data = data
        obj._ebounds = Ebounds.from_bounds(data.lo_edges, data.hi_edges)

        # set GTI
        if gti is not None:
            if not isinstance(gti, Gti):
                raise TypeError('gti must be of type Gti')
        else:
            gti = GTI.from_bounds(obj.column(3, 'START'),obj.column(3, 'STOP'))
        obj._gti = gti

        # update times to be relative to ...if trigtime is set
        if trigger_time is not None:
            if trigger_time < 0.0:
                raise ValueError('trigger_time must be non-negative')
            obj._trigtime = trigger_time

        # set headers
        if headers is not None:
            if not isinstance(headers, PhaHeaders):
                raise TypeError('headers must be of type FileHeaders')
            obj._headers = headers
        else:
            obj._headers = header_type()
            tstart, tstop = obj._gti.range
            obj._headers['PRIMARY']['TSTART'] = tstart
            obj._headers['PRIMARY']['TSTOP'] = tstop
            obj._headers['PRIMARY']['TRIGTIME'] = trigger_time

            obj._headers['SPECTRUM']['DETCHANS'] = data.size
            obj._headers['SPECTRUM']['EXPOSURE'] = obj._data.exposure
            obj._headers['SPECTRUM']['TELAPSE'] = tstop-tstart

            obj._headers['EBOUNDS']['DETCHANS'] = data.size

        # set the channel mask
        # if no channel mask is given, assume zero-count channels are bad
        if channel_mask is None:
            channel_mask = np.zeros(data.size, dtype=bool)
            channel_mask[data.counts > 0] = True
        try:
            iter(channel_mask)
            channel_mask = np.asarray(channel_mask).flatten().astype(bool)
        except:
            raise TypeError('channel_mask must be a Boolean array')
        if channel_mask.size != obj._data.size:
            raise ValueError('channel_mask must be the same size as the ' \
                             'number of data bins')
        obj._channel_mask = channel_mask

        return obj


    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a BAT Pha FITS file and return the BatPha object

        Args:
            file_path (str): The file path of the FITS file

        Returns:
            (:class:`BatPha`)
        """

        obj = super(Pha, cls).open(file_path, **kwargs)
        trigtime = None

        # get the headers
        hdrs = [hdu.header for hdu in obj.hdulist]

        if 'TRIGTIME' in hdrs[0].keys():
            headers = PhaHeaders.from_headers(hdrs)
            trigtime = float(headers['PRIMARY']['TRIGTIME'])

        else:
            headers = PhaHeaders.from_headers(hdrs)

        #if 'TSTART' in hdrs[0].keys():
        tstart = float(headers['PRIMARY']['TSTART'])
        tstop =  float(headers['PRIMARY']['TSTOP'])


        # the channel energy bounds
        ebounds = Ebounds.from_bounds(obj.column(2, 'E_MIN'),
                                      obj.column(2, 'E_MAX'))

        channel = obj.column(1,'CHANNEL')
        rate = obj.column(1, 'RATE')
        stat_err = obj.column(1, 'STAT_ERR')
        sys_err = obj.column(1, 'SYS_ERR')

        #the good time intervals
        stdgti_start = obj.column(3, 'START')
        stdgti_stop = obj.column(3, 'STOP')
        if trigtime is not None:
            stdgti_start -= trigtime
            stdgti_stop -= trigtime
        stdgti = Gti.from_bounds(stdgti_start, stdgti_stop)

        exposure = headers['SPECTRUM']['EXPOSURE']
        counts = obj.column(1, 'RATE') * exposure
        data = EnergyBins(counts, obj.column(2, 'E_MIN'), obj.column(2, 'E_MAX'), exposure,
                        )
        return cls.from_data(data, gti=stdgti, trigger_time=trigtime,
                                filename=obj.filename, headers=headers)


    def _build_hdulist(self):

        # create FITS and primary header
        hdulist = fits.HDUList()
        primary_hdu = fits.PrimaryHDU(header=self.headers['PRIMARY'])
        for key, val in self.headers['PRIMARY'].items():
            primary_hdu.header[key] = val
        hdulist.append(primary_hdu)


        # the spectrum extension
        spectrum_hdu = self._spectrum_table()
        hdulist.append(spectrum_hdu)

        # the ebounds extension
        ebounds_hdu = self._ebounds_table()
        hdulist.append(ebounds_hdu)

        # the GTI extension
        stdgti_hdu = self._gti_table()
        hdulist.append(stdgti_hdu)

        return hdulist

    def _build_headers(self, trigtime, tstart, tstop, num_chans):

        headers = self.headers.copy()
        for hdu in headers:
            hdu['TSTART'] = tstart
            hdu['TSTOP'] = tstop
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

    def _spectrum_table(self):
        chan_col = fits.Column(name='CHANNEL', format='1I',
                               array=np.arange(self.num_chans, dtype=int))
        rates_col = fits.Column(name='RATE', format='1D', unit='count/s',
                                array=self.data.rates)
        staterr_col = fits.Column(name='STAT_ERR', format='1D', unit='count/s',
                                  array=self.data.rate_uncertainty)
        syserr_col = fits.Column(name='SYS_ERR', format='1D', unit='count/s',
                                  array=self.data.rate_uncertainty)

        hdu = fits.BinTableHDU.from_columns([chan_col, rates_col, staterr_col, syserr_col],
                                            header=self.headers['SPECTRUM'])
        for key, val in self.headers['SPECTRUM'].items():
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
                                            header=self.headers['STDGTI'])

        for key, val in self.headers['STDGTI'].items():
            hdu.header[key] = val
        hdu.header.comments['TIMEZERO'] = 'Zero-point offset for TIME column'

        return hdu
