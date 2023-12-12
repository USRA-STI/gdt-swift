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
import unittest
from tempfile import TemporaryDirectory
#from gdt.core import data_path
from gdt.missions.swift.bat.response import *
from gdt.core.spectra.functions import PowerLaw
from pathlib import Path

base_path = Path()
data_path = base_path.joinpath('test_data')
as_rsp = data_path / 'sw00974827000bevas.rsp'
ps_rsp = data_path / 'sw00974827000bevps.rsp'

@unittest.skipIf(not as_rsp.exists(), "test files aren't downloaded. run gdt-download-data.")
class TestBatRsp_As(unittest.TestCase):

    def setUp(self):
        self.rsp =BatRsp.open(as_rsp)

    def tearDown(self):
        self.rsp.close()

    def test_num_chans(self):
        self.assertEqual(self.rsp.num_chans, 80)

    def test_num_ebins(self):
        self.assertEqual(self.rsp.num_ebins, 204)

    def test_tcent(self):
        self.assertAlmostEqual(self.rsp.tcent,  91.47029000520706, places=3)

    def test_trigtime(self):
        self.assertAlmostEqual(self.rsp.trigtime, 612354468.864, places=6)

    def test_tstart(self):
        self.assertAlmostEqual(self.rsp.tstart,69.73658001422882, places=3)

    def test_tstop(self):
        self.assertAlmostEqual(self.rsp.tstop, 113.2039999961853, places=3)

    def test_fold_spectrum(self):
        ebins = self.rsp.fold_spectrum(PowerLaw().fit_eval, (0.01, -2.2), exposure=2.0)
        self.assertEqual(ebins.size, self.rsp.num_chans)
        self.assertEqual(ebins.exposure[0], 2.0)

    def test_rebin(self):
        rsp = self.rsp.rebin(factor=2)
        self.assertEqual(rsp.num_chans, self.rsp.num_chans // 2)
        self.assertEqual(rsp.num_ebins, self.rsp.num_ebins)

    def test_resample(self):
        rsp = self.rsp.resample(num_photon_bins=102)
        self.assertEqual(rsp.num_chans, self.rsp.num_chans)
        self.assertEqual(rsp.num_ebins, self.rsp.num_ebins // 2)

    def test_write(self):
        #with TemporaryDirectory() as this_path:
            self.rsp.write('temp/', overwrite=True)
            rsp = BatRsp.open(os.path.join('temp/', self.rsp.filename))

            for i in range(self.rsp.num_chans):
                self.assertListEqual(rsp.drm.matrix[:, i].tolist(),
                                     self.rsp.drm.matrix[:, i].tolist())
                self.assertListEqual(rsp.ebounds.low_edges(), self.rsp.ebounds.low_edges())
            self.assertListEqual(rsp.ebounds.high_edges(), self.rsp.ebounds.high_edges())
            self.assertEqual(rsp.trigtime, self.rsp.trigtime)
            self.assertEqual(rsp.tstart, self.rsp.tstart)
            self.assertEqual(rsp.tstop, self.rsp.tstop)
            rsp.close()


@unittest.skipIf(not ps_rsp.exists(), "test files aren't downloaded. run gdt-download-data.")
class TestBatRsp_Ps(unittest.TestCase):

    def setUp(self):
        self.rsp =BatRsp.open(ps_rsp)

    def tearDown(self):
        self.rsp.close()

    def test_num_chans(self):
        self.assertEqual(self.rsp.num_chans, 80)

    def test_num_ebins(self):
        self.assertEqual(self.rsp.num_ebins, 204)

    def test_tcent(self):
        self.assertAlmostEqual(self.rsp.tcent,  4.974300026893616, places=3)

    def test_trigtime(self):
        self.assertAlmostEqual(self.rsp.trigtime, 612354468.864, places=6)

    def test_tstart(self):
        self.assertAlmostEqual(self.rsp.tstart, -0.5879999399185181, places=3)

    def test_tstop(self):
        self.assertAlmostEqual(self.rsp.tstop, 10.53659999370575, places=3)

    def test_fold_spectrum(self):
        ebins = self.rsp.fold_spectrum(PowerLaw().fit_eval, (0.01, -2.2), exposure=2.0)
        self.assertEqual(ebins.size, self.rsp.num_chans)
        self.assertEqual(ebins.exposure[0], 2.0)

    def test_rebin(self):
        rsp = self.rsp.rebin(factor=2)
        self.assertEqual(rsp.num_chans, self.rsp.num_chans // 2)
        self.assertEqual(rsp.num_ebins, self.rsp.num_ebins)

    def test_resample(self):
        rsp = self.rsp.resample(num_photon_bins=102)
        self.assertEqual(rsp.num_chans, self.rsp.num_chans)
        self.assertEqual(rsp.num_ebins, self.rsp.num_ebins // 2)

    def test_write(self):
        #with TemporaryDirectory() as this_path:
            self.rsp.write('temp/', overwrite=True)
            rsp = BatRsp.open(os.path.join('temp/', self.rsp.filename))

            for i in range(self.rsp.num_chans):
                self.assertListEqual(rsp.drm.matrix[:, i].tolist(),
                                     self.rsp.drm.matrix[:, i].tolist())
                self.assertListEqual(rsp.ebounds.low_edges(), self.rsp.ebounds.low_edges())
            self.assertListEqual(rsp.ebounds.high_edges(), self.rsp.ebounds.high_edges())
            self.assertEqual(rsp.trigtime, self.rsp.trigtime)
            self.assertEqual(rsp.tstart, self.rsp.tstart)
            self.assertEqual(rsp.tstop, self.rsp.tstop)
            rsp.close()
