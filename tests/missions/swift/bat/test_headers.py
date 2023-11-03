# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT WITH UNLIMITED RIGHTS
#
# Contract No.: CA 80MSFC17M0022
# Contractor Name: Universities Space Research Association
# Contractor Address: 7178 Columbia Gateway Drive, Columbia, MD 21046
#
# Copyright 2017-2022 by Universities Space Research Association (USRA). All rights reserved.
#
# Developed by: William Cleveland and Adam Goldstein
#               Universities Space Research Association
#               Science and Technology Institute
#               https://sti.usra.edu
#
# Developed by: Daniel Kocevski
#               National Aeronautics and Space Administration (NASA)
#               Marshall Space Flight Center
#               Astrophysics Branch (ST-12)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing permissions and limitations under the
# License.
#

import os
import numpy as np
import unittest

from gdt.missions.swift.bat.headers import *


class TestSaoHeaders(unittest.TestCase):
    def setUp(self):
        self.headers = SaoHeaders()

    def test_primary(self):
        hdr = self.headers[0]
        self.assertTrue('DATE-OBS' in hdr.keys())
        self.assertTrue('TIME-OBS' in hdr.keys())
        self.assertTrue('DATE-END' in hdr.keys())
        self.assertTrue('TIME-END' in hdr.keys())
        self.assertTrue('TSTART' in hdr.keys())
        self.assertTrue('TSTOP' in hdr.keys())
        self.assertTrue('DELTAT' in hdr.keys())
        self.assertTrue('RA_NOM' in hdr.keys())
        self.assertTrue('DEC_NOM' in hdr.keys())
        self.assertTrue('TELESCOP' in hdr.keys())
        self.assertEqual(hdr['TELESCOP'], 'SWIFT')
        self.assertTrue('TIMESYS' in hdr.keys())
        self.assertEqual(hdr['TIMESYS'], 'TT')
        self.assertTrue('TIMEUNIT' in hdr.keys())
        self.assertEqual(hdr['TIMEUNIT'], 's')
        self.assertTrue('MJDREFI' in hdr.keys())
        self.assertEqual(hdr['MJDREFI'], 51910)
        self.assertTrue('MJDREFF' in hdr.keys())
        self.assertEqual(hdr['MJDREFF'], '7.428703703703703e-4')
        self.assertTrue('EQUINOX' in hdr.keys())
        self.assertEqual(hdr['EQUINOX'], 2000.0)
        self.assertTrue('RADECSYS' in hdr.keys())
        self.assertEqual(hdr['RADECSYS'], 'FK5')
        self.assertTrue('CREATOR' in hdr.keys())
        self.assertTrue('ORIGIN' in hdr.keys())
        self.assertEqual(hdr['ORIGIN'], 'GSFC')
        self.assertTrue('DATE' in hdr.keys())
        self.assertTrue('CHECKSUM' in hdr.keys())
        self.assertTrue('DATASUM' in hdr.keys())
        self.assertTrue('PROCVER' in hdr.keys())
        self.assertTrue('SOFTVER' in hdr.keys())
        self.assertTrue('CALDBVER' in hdr.keys())
        self.assertTrue('CLOCKAPP' in hdr.keys())
        self.assertTrue('OBS_ID' in hdr.keys())
        self.assertTrue('SEQPNUM' in hdr.keys())
        self.assertTrue('TARG_ID' in hdr.keys())
        self.assertTrue('SEG_NUM' in hdr.keys())
        self.assertTrue('OBJECT' in hdr.keys())
        self.assertTrue('RA_OBJ' in hdr.keys())
        self.assertTrue('DEC_OBJ' in hdr.keys())
        self.assertTrue('RA_PNT' in hdr.keys())
        self.assertTrue('DEC_PNT' in hdr.keys())
        self.assertTrue('PA_PNT' in hdr.keys())
        self.assertTrue('TRIGTIME' in hdr.keys())
        self.assertTrue('UTCFINIT' in hdr.keys())

    def test_prefilter(self):
        hdr = self.headers[1]
        self.assertTrue('EXTNAME' in hdr.keys())
        self.assertEqual(hdr['EXTNAME'], 'PREFILTER')
        self.assertTrue('DATE-OBS' in hdr.keys())
        self.assertTrue('TIME-OBS' in hdr.keys())
        self.assertTrue('DATE-END' in hdr.keys())
        self.assertTrue('TIME-END' in hdr.keys())
        self.assertTrue('TSTART' in hdr.keys())
        self.assertTrue('TSTOP' in hdr.keys())
        self.assertTrue('DELTAT' in hdr.keys())
        self.assertTrue('RA_NOM' in hdr.keys())
        self.assertTrue('DEC_NOM' in hdr.keys())
        self.assertTrue('TELESCOP' in hdr.keys())
        self.assertEqual(hdr['TELESCOP'], 'SWIFT')
        self.assertTrue('TIMESYS' in hdr.keys())
        self.assertEqual(hdr['TIMESYS'], 'TT')
        self.assertTrue('TIMEUNIT' in hdr.keys())
        self.assertEqual(hdr['TIMEUNIT'], 's')
        self.assertTrue('MJDREFI' in hdr.keys())
        self.assertEqual(hdr['MJDREFI'], 51910)
        self.assertTrue('MJDREFF' in hdr.keys())
        self.assertEqual(hdr['MJDREFF'], '7.428703703703703e-4')
        self.assertTrue('EQUINOX' in hdr.keys())
        self.assertEqual(hdr['EQUINOX'], 2000.0)
        self.assertTrue('RADECSYS' in hdr.keys())
        self.assertEqual(hdr['RADECSYS'], 'FK5')
        self.assertTrue('CREATOR' in hdr.keys())
        self.assertTrue('ORIGIN' in hdr.keys())
        self.assertEqual(hdr['ORIGIN'], 'GSFC')
        self.assertTrue('DATE' in hdr.keys())
        self.assertTrue('CHECKSUM' in hdr.keys())
        self.assertTrue('DATASUM' in hdr.keys())
        self.assertTrue('PROCVER' in hdr.keys())
        self.assertTrue('SOFTVER' in hdr.keys())
        self.assertTrue('CALDBVER' in hdr.keys())
        self.assertTrue('TIERRELA' in hdr.keys())
        self.assertEqual(hdr['TIERRELA'], 1.0E-8)
        self.assertTrue('TIERABSO' in hdr.keys())
        self.assertEqual(hdr['TIERABSO'], 1.0)
        self.assertTrue('OBS_ID' in hdr.keys())
        self.assertTrue('SEQPNUM' in hdr.keys())
        self.assertTrue('TARG_ID' in hdr.keys())
        self.assertTrue('SEG_NUM' in hdr.keys())
        self.assertTrue('OBJECT' in hdr.keys())
        self.assertTrue('RA_OBJ' in hdr.keys())
        self.assertTrue('DEC_OBJ' in hdr.keys())
        self.assertTrue('RA_PNT' in hdr.keys())
        self.assertTrue('DEC_PNT' in hdr.keys())
        self.assertTrue('PA_PNT' in hdr.keys())
        self.assertTrue('TRIGTIME' in hdr.keys())
        self.assertTrue('UTCFINIT' in hdr.keys())




class TestPhaHeaders(unittest.TestCase):
    def setUp(self):
        self.headers = PhaHeaders()

    def test_primary(self):
        hdr = self.headers[0]
        self.assertTrue('TELESCOP' in hdr.keys())
        self.assertEqual(hdr['TELESCOP'], 'SWIFT')
        self.assertTrue('INSTRUME' in hdr.keys())
        self.assertEqual(hdr['INSTRUME'], 'BAT')
        self.assertTrue('OBS_ID' in hdr.keys())
        self.assertTrue('TARG_ID' in hdr.keys())
        self.assertTrue('SEG_NUM' in hdr.keys())
        self.assertTrue('TIMESYS' in hdr.keys())
        self.assertEqual(hdr['TIMESYS'], 'TT')
        self.assertTrue('MJDREFI' in hdr.keys())
        self.assertEqual(hdr['MJDREFI'], 51910)
        self.assertTrue('MJDREFF' in hdr.keys())
        self.assertEqual(hdr['MJDREFF'], '7.428703703703703e-4')
        self.assertTrue('CLOCKAPP' in hdr.keys())
        self.assertTrue('TIMEUNIT' in hdr.keys())
        self.assertEqual(hdr['TIMEUNIT'], 's')
        self.assertTrue('TSTART' in hdr.keys())
        self.assertTrue('TSTOP' in hdr.keys())
        self.assertTrue('DATE-OBS' in hdr.keys())
        self.assertTrue('DATE-END' in hdr.keys())
        self.assertTrue('ORIGIN' in hdr.keys())
        self.assertEqual(hdr['ORIGIN'], 'NASA/GSFC')
        self.assertTrue('CREATOR' in hdr.keys())
        self.assertTrue('TLM2FITS' in hdr.keys())
        self.assertTrue('DATE' in hdr.keys())
        self.assertTrue('NEVENTS' in hdr.keys())
        self.assertTrue('DATAMODE' in hdr.keys())
        self.assertTrue('TIMEREF' in hdr.keys())
        self.assertEqual(hdr['TIMEREF'], 'LOCAL')
        self.assertTrue('EQUINOX' in hdr.keys())
        self.assertTrue('RADECSYS' in hdr.keys())
        self.assertTrue('USER' in hdr.keys())
        self.assertTrue('FILIN001' in hdr.keys())
        self.assertTrue('TIMEZERO' in hdr.keys())
        self.assertTrue('CHECKSUM' in hdr.keys())
        self.assertTrue('DATASUM' in hdr.keys())
        self.assertTrue('PROCVER' in hdr.keys())
        self.assertTrue('SOFTVER' in hdr.keys())
        self.assertTrue('CALDBVER' in hdr.keys())
        self.assertTrue('SEQPNUM' in hdr.keys())
        self.assertTrue('RA_OBJ' in hdr.keys())
        self.assertTrue('DEC_OBJ' in hdr.keys())
        self.assertTrue('RA_PNT' in hdr.keys())
        self.assertTrue('DEC_PNT' in hdr.keys())
        self.assertTrue('PA_PNT' in hdr.keys())
        self.assertTrue('TRIGTIME' in hdr.keys())
        self.assertTrue('CATSRC' in hdr.keys())
        self.assertTrue('ATTFLAG' in hdr.keys())
        self.assertTrue('UTCFINIT' in hdr.keys())

    def test_spectrum(self):
        hdr = self.headers[1]
        self.assertTrue('EXTNAME' in hdr.keys())
        self.assertEqual(hdr['EXTNAME'], 'SPECTRUM')
        self.assertTrue('HDUCLASS' in hdr.keys())
        self.assertTrue('HDUCLAS1' in hdr.keys())
        self.assertTrue('GAINAPP' in hdr.keys())
        self.assertTrue('TIMESYS' in hdr.keys())
        self.assertEqual(hdr['TIMESYS'], 'TT')
        self.assertTrue('MJDREFI' in hdr.keys())
        self.assertEqual(hdr['MJDREFI'], 51910)
        self.assertTrue('MJDREFF' in hdr.keys())
        self.assertEqual(hdr['MJDREFF'], '7.428703703703703e-4')
        self.assertTrue('TIMEREF' in hdr.keys())
        self.assertEqual(hdr['TIMEREF'], 'LOCAL')
        self.assertTrue('TASSIGN' in hdr.keys())
        self.assertTrue('TIMEUNIT' in hdr.keys())
        self.assertEqual(hdr['TIMEUNIT'], 's')
        self.assertTrue('TIERRELA' in hdr.keys())
        self.assertTrue('TIERABSO' in hdr.keys())
        self.assertTrue('TSTART' in hdr.keys())
        self.assertTrue('TSTOP' in hdr.keys())
        self.assertTrue('DATE-OBS' in hdr.keys())
        self.assertTrue('DATE-END' in hdr.keys())
        self.assertTrue('CLOCKAPP' in hdr.keys())
        self.assertTrue('TELAPSE' in hdr.keys())
        self.assertTrue('ONTIME' in hdr.keys())
        self.assertTrue('LIVETIME' in hdr.keys())
        self.assertTrue('CLOCKAPP' in hdr.keys())
        self.assertTrue('EXPOSURE' in hdr.keys())
        self.assertTrue('DEADC' in hdr.keys())
        self.assertTrue('TIMEPIXR' in hdr.keys())
        self.assertTrue('TIMEDEL' in hdr.keys())
        self.assertTrue('TELESCOP' in hdr.keys())
        self.assertEqual(hdr['TELESCOP'], 'SWIFT')
        self.assertTrue('INSTRUME' in hdr.keys())
        self.assertEqual(hdr['INSTRUME'], 'BAT')
        self.assertTrue('DATAMODE' in hdr.keys())
        self.assertTrue('OBS_ID' in hdr.keys())
        self.assertTrue('TARG_ID' in hdr.keys())
        self.assertTrue('SEG_NUM' in hdr.keys())
        self.assertTrue('EQUINOX' in hdr.keys())
        self.assertTrue('RADECSYS' in hdr.keys())
        self.assertTrue('OBS_MODE' in hdr.keys())
        self.assertTrue('ORIGIN' in hdr.keys())
        self.assertEqual(hdr['ORIGIN'], 'NASA/GSFC')
        self.assertTrue('CREATOR' in hdr.keys())
        self.assertTrue('TLM2FITS' in hdr.keys())
        self.assertTrue('DATE' in hdr.keys())
        self.assertTrue('PROCVER' in hdr.keys())
        self.assertTrue('SOFTVER' in hdr.keys())
        self.assertTrue('CALDBVER' in hdr.keys())
        self.assertTrue('SEQPNUM' in hdr.keys())
        self.assertTrue('RA_OBJ' in hdr.keys())
        self.assertTrue('DEC_OBJ' in hdr.keys())
        self.assertTrue('RA_PNT' in hdr.keys())
        self.assertTrue('DEC_PNT' in hdr.keys())
        self.assertTrue('PA_PNT' in hdr.keys())
        self.assertTrue('CATSRC' in hdr.keys())
        self.assertTrue('ATTFLAG' in hdr.keys())
        self.assertTrue('UTCFINIT' in hdr.keys())
        self.assertTrue('CHECKSUM' in hdr.keys())
        self.assertTrue('DATASUM' in hdr.keys())



    def test_ebounds(self):
        hdr = self.headers[2]
        self.assertTrue('EXTNAME' in hdr.keys())
        self.assertEqual(hdr['EXTNAME'], 'EBOUNDS')
        self.assertTrue('HDUCLASS' in hdr.keys())
        self.assertTrue('HDUCLAS1' in hdr.keys())
        self.assertTrue('GAINAPP' in hdr.keys())
        self.assertTrue('TIMESYS' in hdr.keys())
        self.assertEqual(hdr['TIMESYS'], 'TT')
        self.assertTrue('MJDREFI' in hdr.keys())
        self.assertEqual(hdr['MJDREFI'], 51910)
        self.assertTrue('MJDREFF' in hdr.keys())
        self.assertEqual(hdr['MJDREFF'], '7.428703703703703e-4')
        self.assertTrue('TIMEREF' in hdr.keys())
        self.assertEqual(hdr['TIMEREF'], 'LOCAL')
        self.assertTrue('TASSIGN' in hdr.keys())
        self.assertTrue('TIMEUNIT' in hdr.keys())
        self.assertEqual(hdr['TIMEUNIT'], 's')
        self.assertTrue('TIERRELA' in hdr.keys())
        self.assertTrue('TIERABSO' in hdr.keys())
        self.assertTrue('TSTART' in hdr.keys())
        self.assertTrue('TSTOP' in hdr.keys())
        self.assertTrue('DATE-OBS' in hdr.keys())
        self.assertTrue('DATE-END' in hdr.keys())
        self.assertTrue('CLOCKAPP' in hdr.keys())
        self.assertTrue('DEADC' in hdr.keys())
        self.assertTrue('TIMEPIXR' in hdr.keys())
        self.assertTrue('TIMEDEL' in hdr.keys())
        self.assertTrue('TELESCOP' in hdr.keys())
        self.assertEqual(hdr['TELESCOP'], 'SWIFT')
        self.assertTrue('INSTRUME' in hdr.keys())
        self.assertEqual(hdr['INSTRUME'], 'BAT')
        self.assertTrue('DATAMODE' in hdr.keys())
        self.assertTrue('OBS_ID' in hdr.keys())
        self.assertTrue('TARG_ID' in hdr.keys())
        self.assertTrue('SEG_NUM' in hdr.keys())
        self.assertTrue('EQUINOX' in hdr.keys())
        self.assertTrue('RADECSYS' in hdr.keys())
        self.assertTrue('OBS_MODE' in hdr.keys())
        self.assertTrue('ORIGIN' in hdr.keys())
        self.assertEqual(hdr['ORIGIN'], 'NASA/GSFC')
        self.assertTrue('CREATOR' in hdr.keys())
        self.assertTrue('TLM2FITS' in hdr.keys())
        self.assertTrue('DATE' in hdr.keys())
        self.assertTrue('PROCVER' in hdr.keys())
        self.assertTrue('SOFTVER' in hdr.keys())
        self.assertTrue('CALDBVER' in hdr.keys())
        self.assertTrue('SEQPNUM' in hdr.keys())
        self.assertTrue('RA_OBJ' in hdr.keys())
        self.assertTrue('DEC_OBJ' in hdr.keys())
        self.assertTrue('RA_PNT' in hdr.keys())
        self.assertTrue('DEC_PNT' in hdr.keys())
        self.assertTrue('PA_PNT' in hdr.keys())
        self.assertTrue('CATSRC' in hdr.keys())
        self.assertTrue('ATTFLAG' in hdr.keys())
        self.assertTrue('UTCFINIT' in hdr.keys())
        self.assertTrue('CHECKSUM' in hdr.keys())
        self.assertTrue('DATASUM' in hdr.keys())


    def test_stdgti(self):
        hdr = self.headers[3]
        self.assertTrue('EXTNAME' in hdr.keys())
        self.assertEqual(hdr['EXTNAME'], 'STDGTI')
        self.assertTrue('HDUCLASS' in hdr.keys())
        self.assertTrue('HDUCLAS1' in hdr.keys())
        self.assertTrue('HDUCLAS2' in hdr.keys())
        self.assertTrue('HDUVERS' in hdr.keys())
        self.assertTrue('TIMEZERO' in hdr.keys())
        self.assertTrue('MJDREF' in hdr.keys())
        self.assertTrue('GAINAPP' in hdr.keys())
        self.assertTrue('TIMESYS' in hdr.keys())
        self.assertEqual(hdr['TIMESYS'], 'TT')
        self.assertTrue('TIMEREF' in hdr.keys())
        self.assertEqual(hdr['TIMEREF'], 'LOCAL')
        self.assertTrue('TASSIGN' in hdr.keys())
        self.assertTrue('TIMEUNIT' in hdr.keys())
        self.assertEqual(hdr['TIMEUNIT'], 's')
        self.assertTrue('TIERRELA' in hdr.keys())
        self.assertTrue('TIERABSO' in hdr.keys())
        self.assertTrue('DATE-OBS' in hdr.keys())
        self.assertTrue('DATE-END' in hdr.keys())
        self.assertTrue('CLOCKAPP' in hdr.keys())
        self.assertTrue('DEADC' in hdr.keys())
        self.assertTrue('TIMEPIXR' in hdr.keys())
        self.assertTrue('TIMEDEL' in hdr.keys())
        self.assertTrue('TELESCOP' in hdr.keys())
        self.assertEqual(hdr['TELESCOP'], 'SWIFT')
        self.assertTrue('INSTRUME' in hdr.keys())
        self.assertEqual(hdr['INSTRUME'], 'BAT')
        self.assertTrue('DATAMODE' in hdr.keys())
        self.assertTrue('OBS_ID' in hdr.keys())
        self.assertTrue('TARG_ID' in hdr.keys())
        self.assertTrue('SEG_NUM' in hdr.keys())
        self.assertTrue('EQUINOX' in hdr.keys())
        self.assertTrue('RADECSYS' in hdr.keys())
        self.assertTrue('OBS_MODE' in hdr.keys())
        self.assertTrue('ORIGIN' in hdr.keys())
        self.assertEqual(hdr['ORIGIN'], 'NASA/GSFC')
        self.assertTrue('CREATOR' in hdr.keys())
        self.assertTrue('TLM2FITS' in hdr.keys())
        self.assertTrue('DATE' in hdr.keys())
        self.assertTrue('OBJECT' in hdr.keys())
        self.assertTrue('MJD-OBS' in hdr.keys())
        self.assertTrue('USER' in hdr.keys())
        self.assertTrue('FILIN001' in hdr.keys())
        self.assertTrue('NPIXSOU' in hdr.keys())
        self.assertTrue('PROCVER' in hdr.keys())
        self.assertTrue('SEQPNUM' in hdr.keys())
        self.assertTrue('RA_OBJ' in hdr.keys())
        self.assertTrue('DEC_OBJ' in hdr.keys())
        self.assertTrue('RA_PNT' in hdr.keys())
        self.assertTrue('DEC_PNT' in hdr.keys())
        self.assertTrue('PA_PNT' in hdr.keys())
        self.assertTrue('CATSRC' in hdr.keys())
        self.assertTrue('ATTFLAG' in hdr.keys())
        self.assertTrue('UTCFINIT' in hdr.keys())
        self.assertTrue('CHECKSUM' in hdr.keys())
        self.assertTrue('DATASUM' in hdr.keys())

class TestRspHeaders(unittest.TestCase):
    def setUp(self):
        self.headers = RspHeaders()

    def test_primary(self):
        hdr = self.headers[0]
        self.assertTrue('PROCVER' in hdr.keys())
        self.assertTrue('SOFTVER' in hdr.keys())
        self.assertTrue('CALDBVER' in hdr.keys())
        self.assertTrue('TIMESYS' in hdr.keys())
        self.assertEqual(hdr['TIMESYS'], 'TT')
        self.assertTrue('MJDREFI' in hdr.keys())
        self.assertEqual(hdr['MJDREFI'], 51910)
        self.assertTrue('MJDREFF' in hdr.keys())
        self.assertEqual(hdr['MJDREFF'], '7.428703703703703e-4')
        self.assertTrue('CLOCKAPP' in hdr.keys())
        self.assertTrue('TIMEUNIT' in hdr.keys())
        self.assertEqual(hdr['TIMEUNIT'], 's')
        self.assertTrue('OBS_ID' in hdr.keys())
        self.assertTrue('SEQPNUM' in hdr.keys())
        self.assertTrue('RA_OBJ' in hdr.keys())
        self.assertTrue('DEC_OBJ' in hdr.keys())
        self.assertTrue('RA_PNT' in hdr.keys())
        self.assertTrue('DEC_PNT' in hdr.keys())
        self.assertTrue('PA_PNT' in hdr.keys())
        self.assertTrue('TRIGTIME' in hdr.keys())
        self.assertTrue('CATSRC' in hdr.keys())
        self.assertTrue('ATTFLAG' in hdr.keys())
        self.assertTrue('CHECKSUM' in hdr.keys())
        self.assertTrue('DATASUM' in hdr.keys())

    def test_spec(self):
        hdr = self.headers[1]
        self.assertTrue('EXTNAME' in hdr.keys())
        self.assertEqual(hdr['EXTNAME'], 'SPECRESP MATRIX')
        self.assertTrue('HDUCLASS' in hdr.keys())
        self.assertTrue('HDUCLAS1' in hdr.keys())
        self.assertTrue('GAINAPP' in hdr.keys())
        self.assertTrue('TIMESYS' in hdr.keys())
        self.assertEqual(hdr['TIMESYS'], 'TT')
        self.assertTrue('MJDREFI' in hdr.keys())
        self.assertEqual(hdr['MJDREFI'], 51910)
        self.assertTrue('MJDREFF' in hdr.keys())
        self.assertEqual(hdr['MJDREFF'], '7.428703703703703e-4')
        self.assertTrue('TIMEREF' in hdr.keys())
        self.assertTrue('TASSIGN' in hdr.keys())
        self.assertTrue('TIMEUNIT' in hdr.keys())
        self.assertEqual(hdr['TIMEUNIT'], 's')
        self.assertTrue('TIERRELA' in hdr.keys())
        self.assertTrue('TIERABSO' in hdr.keys())
        self.assertTrue('TSTART' in hdr.keys())
        self.assertTrue('TSTOP' in hdr.keys())
        self.assertTrue('DATE-OBS' in hdr.keys())
        self.assertTrue('DATE-END' in hdr.keys())
        self.assertTrue('CLOCKAPP' in hdr.keys())
        self.assertTrue('TELAPSE' in hdr.keys())
        self.assertTrue('ONTIME' in hdr.keys())
        self.assertTrue('LIVETIME' in hdr.keys())
        self.assertTrue('EXPOSURE' in hdr.keys())
        self.assertTrue('DEADC' in hdr.keys())
        self.assertTrue('TIMEPIXR' in hdr.keys())
        self.assertTrue('TIMEDEL' in hdr.keys())
        self.assertTrue('TELESCOP' in hdr.keys())
        self.assertEqual(hdr['TELESCOP'], 'SWIFT')
        self.assertTrue('INSTRUME' in hdr.keys())
        self.assertEqual(hdr['INSTRUME'], 'BAT')
        self.assertTrue('DATAMODE' in hdr.keys())
        self.assertTrue('OBS_ID' in hdr.keys())
        self.assertTrue('TARG_ID' in hdr.keys())
        self.assertTrue('SEG_NUM' in hdr.keys())
        self.assertTrue('EQUINOX' in hdr.keys())
        self.assertTrue('RADECSYS' in hdr.keys())
        self.assertTrue('OBS_MODE' in hdr.keys())
        self.assertTrue('ORIGIN' in hdr.keys())
        self.assertEqual(hdr['ORIGIN'], 'NASA/GSFC')
        self.assertTrue('CREATOR' in hdr.keys())
        self.assertTrue('TLM2FITS' in hdr.keys())
        self.assertTrue('DATE' in hdr.keys())
        self.assertTrue('TIMEZERO' in hdr.keys())
        self.assertTrue('OBJECT' in hdr.keys())
        self.assertTrue('MJD-OBS' in hdr.keys())
        self.assertTrue('USER' in hdr.keys())
        self.assertTrue('FILIN001' in hdr.keys())
        self.assertTrue('NPIXSOU' in hdr.keys())
        self.assertTrue('BACKAPP' in hdr.keys())
        self.assertTrue('HDUCLAS2' in hdr.keys())
        self.assertTrue('HDUCLAS3' in hdr.keys())
        self.assertTrue('PHAVERSN' in hdr.keys())
        self.assertTrue('HDUVERS' in hdr.keys())
        self.assertTrue('FLUXMETH' in hdr.keys())
        self.assertTrue('PROCVER' in hdr.keys())
        self.assertTrue('SOFTVER' in hdr.keys())
        self.assertTrue('CALDBVER' in hdr.keys())
        self.assertTrue('SEQPNUM' in hdr.keys())
        self.assertTrue('RA_OBJ' in hdr.keys())
        self.assertTrue('DEC_OBJ' in hdr.keys())
        self.assertTrue('RA_PNT' in hdr.keys())
        self.assertTrue('DEC_PNT' in hdr.keys())
        self.assertTrue('PA_PNT' in hdr.keys())
        self.assertTrue('CATSRC' in hdr.keys())
        self.assertTrue('ATTFLAG' in hdr.keys())
        self.assertTrue('UTCFINIT' in hdr.keys())
        self.assertTrue('CHECKSUM' in hdr.keys())
        self.assertTrue('DATASUM' in hdr.keys())

    def test_ebounds(self):
        hdr = self.headers[2]
        self.assertTrue('EXTNAME' in hdr.keys())
        self.assertEqual(hdr['EXTNAME'], 'EBOUNDS')
        self.assertTrue('HDUCLASS' in hdr.keys())
        self.assertTrue('HDUCLAS1' in hdr.keys())
        self.assertTrue('GAINAPP' in hdr.keys())
        self.assertTrue('TIMESYS' in hdr.keys())
        self.assertEqual(hdr['TIMESYS'], 'TT')
        self.assertTrue('MJDREFI' in hdr.keys())
        self.assertEqual(hdr['MJDREFI'], 51910)
        self.assertTrue('MJDREFF' in hdr.keys())
        self.assertEqual(hdr['MJDREFF'], '7.428703703703703e-4')
        self.assertTrue('TIMEREF' in hdr.keys())
        self.assertTrue('TASSIGN' in hdr.keys())
        self.assertTrue('TIMEUNIT' in hdr.keys())
        self.assertEqual(hdr['TIMEUNIT'], 's')
        self.assertTrue('TIERRELA' in hdr.keys())
        self.assertTrue('TIERABSO' in hdr.keys())
        self.assertTrue('TSTART' in hdr.keys())
        self.assertTrue('TSTOP' in hdr.keys())
        self.assertTrue('DATE-OBS' in hdr.keys())
        self.assertTrue('DATE-END' in hdr.keys())
        self.assertTrue('CLOCKAPP' in hdr.keys())
        self.assertTrue('TELAPSE' in hdr.keys())
        self.assertTrue('ONTIME' in hdr.keys())
        self.assertTrue('LIVETIME' in hdr.keys())
        self.assertTrue('EXPOSURE' in hdr.keys())
        self.assertTrue('DEADC' in hdr.keys())
        self.assertTrue('TIMEPIXR' in hdr.keys())
        self.assertTrue('TIMEDEL' in hdr.keys())
        self.assertTrue('TELESCOP' in hdr.keys())
        self.assertEqual(hdr['TELESCOP'], 'SWIFT')
        self.assertTrue('INSTRUME' in hdr.keys())
        self.assertEqual(hdr['INSTRUME'], 'BAT')
        self.assertTrue('DATAMODE' in hdr.keys())
        self.assertTrue('OBS_ID' in hdr.keys())
        self.assertTrue('TARG_ID' in hdr.keys())
        self.assertTrue('SEG_NUM' in hdr.keys())
        self.assertTrue('EQUINOX' in hdr.keys())
        self.assertTrue('RADECSYS' in hdr.keys())
        self.assertTrue('OBS_MODE' in hdr.keys())
        self.assertTrue('ORIGIN' in hdr.keys())
        self.assertEqual(hdr['ORIGIN'], 'NASA/GSFC')
        self.assertTrue('CREATOR' in hdr.keys())
        self.assertTrue('TLM2FITS' in hdr.keys())
        self.assertTrue('DATE' in hdr.keys())
        self.assertTrue('TIMEZERO' in hdr.keys())
        self.assertTrue('OBJECT' in hdr.keys())
        self.assertTrue('MJD-OBS' in hdr.keys())
        self.assertTrue('USER' in hdr.keys())
        self.assertTrue('FILIN001' in hdr.keys())
        self.assertTrue('NPIXSOU' in hdr.keys())
        self.assertTrue('BACKAPP' in hdr.keys())
        self.assertTrue('HDUCLAS2' in hdr.keys())
        self.assertTrue('HDUCLAS3' in hdr.keys())
        self.assertTrue('PHAVERSN' in hdr.keys())
        self.assertTrue('HDUVERS' in hdr.keys())
        self.assertTrue('FLUXMETH' in hdr.keys())
        self.assertTrue('PROCVER' in hdr.keys())
        self.assertTrue('SOFTVER' in hdr.keys())
        self.assertTrue('CALDBVER' in hdr.keys())
        self.assertTrue('SEQPNUM' in hdr.keys())
        self.assertTrue('RA_OBJ' in hdr.keys())
        self.assertTrue('DEC_OBJ' in hdr.keys())
        self.assertTrue('RA_PNT' in hdr.keys())
        self.assertTrue('DEC_PNT' in hdr.keys())
        self.assertTrue('PA_PNT' in hdr.keys())
        self.assertTrue('CATSRC' in hdr.keys())
        self.assertTrue('ATTFLAG' in hdr.keys())
        self.assertTrue('UTCFINIT' in hdr.keys())
        self.assertTrue('CHECKSUM' in hdr.keys())
        self.assertTrue('DATASUM' in hdr.keys())
