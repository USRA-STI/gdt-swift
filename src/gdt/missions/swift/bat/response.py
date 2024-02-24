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
import astropy.io.fits as fits
import numpy as np

from gdt.core.response import *
from gdt.core.data_primitives import Ebounds, ResponseMatrix
from .headers import RspHeaders

__all__ = ['BatRsp']

class BatRsp(Rsp):
    """Class for BAT single-DRM response files.
    """
    @classmethod
    def open(cls, file_path, **kwargs):
        """Read a single-DRM response file from disk.

        Args:
            file_path (str): The file path

        Returns:
           (:class:`BatRsp`)
        """

        obj = super().open(file_path, **kwargs)

        trigtime = None
        # get the headers
        hdrs = [hdu.header for hdu in obj.hdulist]

        if 'TRIGTIME' in hdrs[0].keys():
            headers = RspHeaders.from_headers(hdrs)
            trigtime = float(headers['PRIMARY']['TRIGTIME'])

        else:

            headers = RspHeaders.from_headers(hdrs)


        tstart = headers['SPECRESP MATRIX']['TSTART']
        tstop = headers['SPECRESP MATRIX']['TSTOP']


        ebounds = Ebounds.from_bounds(obj.column(2, 'E_MIN'),
                                      obj.column(2, 'E_MAX'))

        num_ebins =  obj.hdulist['SPECRESP MATRIX'].header['NUMGRP']
        num_chans = obj.hdulist['SPECRESP MATRIX'].header['DETCHANS']
        fchan = np.copy(obj.column(1, 'F_CHAN'))
        nchan = np.copy(obj.column(1, 'N_CHAN'))
        ngrp = np.copy(obj.column(1, 'N_GRP'))


        drm = ResponseMatrix(obj.column(1, 'MATRIX'), obj.column(1, 'ENERG_LO'),
                            obj.column(1, 'ENERG_HI'),  obj.column(2, 'E_MIN'),
                            obj.column(2, 'E_MAX'))

        obj.close()

        obj = cls.from_data(drm, filename=obj.filename,
                            start_time=tstart, stop_time=tstop,
                            trigger_time=trigtime, headers=headers)

        obj._fchan = fchan
        obj._nchan = nchan
        obj._ngrp = ngrp

        return obj

    def _build_hdulist(self):

        # create FITS and primary header
        hdulist = fits.HDUList()
        primary_hdu = fits.PrimaryHDU(header=self.headers['PRIMARY'])
        for key, val in self.headers['PRIMARY'].items():
            primary_hdu.header[key] = val
        hdulist.append(primary_hdu)

        # the drm extension
        drm_hdu = self._drm_table()
        hdulist.append(drm_hdu)

        # the ebounds extension
        ebounds_hdu = self._ebounds_table()
        hdulist.append(ebounds_hdu)

        return hdulist

    def _build_headers(self, num_chans, num_ebins):

        headers = self.headers.copy()
        headers['EBOUNDS']['DETCHANS'] = num_chans
        headers['SPECRESP MATRIX']['DETCHANS'] = num_chans
        headers['SPECRESP MATRIX']['NUMGRP'] = num_ebins
        return headers

    def _ebounds_table(self):
        chan_col = fits.Column(name='CHANNEL', format='I',
                               array=np.arange(self.num_chans, dtype=int))
        emin_col = fits.Column(name='E_MIN', format='E', unit='keV',
                               array=self.ebounds.low_edges())
        emax_col = fits.Column(name='E_MAX', format='E', unit='keV',
                               array=self.ebounds.high_edges())

        hdu = fits.BinTableHDU.from_columns([chan_col, emin_col, emax_col],
                                             header=self.headers['EBOUNDS'])
        for key, val in self.headers['EBOUNDS'].items():
            hdu.header[key] = val

        return hdu

    def _drm_table(self):
        elo_col = fits.Column(name='ENERG_LO', format='E',
                              array=self.drm.photon_bins.low_edges(),
                              unit='keV')
        ehi_col = fits.Column(name='ENERG_HI', format='E',
                              array=self.drm.photon_bins.high_edges(),
                              unit='keV')
        ngrp_col = fits.Column(name='N_GRP', format='I', array=self._ngrp)
        fchan_col = fits.Column(name='F_CHAN', format='I',
                                array=self._fchan)
        nchan_col = fits.Column(name='N_CHAN', format='I',
                                array=self._nchan)
    
        matrix_col = fits.Column(name='MATRIX', array=self.drm.matrix,
                                 format='{}E'.format(self.num_chans),
                                 )

        hdu = fits.BinTableHDU.from_columns([elo_col, ehi_col, ngrp_col,
                                             fchan_col, nchan_col, matrix_col],
                                         header=self.headers['SPECRESP MATRIX'])
        for key, val in self.headers['SPECRESP MATRIX'].items():
            hdu.header[key] = val

        return hdu
