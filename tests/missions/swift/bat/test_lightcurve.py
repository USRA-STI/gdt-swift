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
from pathlib import Path
from tempfile import TemporaryDirectory
from gdt.core import data_path
from gdt.missions.swift.bat.lightcurve import *
from gdt.core.binning.binned import combine_by_factor

base_path = Path()
data_path = base_path.joinpath('test_data')
ones_file = data_path / 'sw00974827000bev1s.lc.gz'
ms_file = data_path / 'sw00974827000bevms.lc.gz'

@unittest.skipIf(not ones_file.exists(), "test files aren't downloaded. run gdt-download-data.")
class TestBatLightcurve(unittest.TestCase):

    def setUp(self):
        self.lc = BatLightcurve.open(ones_file)

    def tearDown(self):
        self.lc.close()

    def test_energy_range(self):
        self.assertAlmostEqual(self.lc.energy_range[0], 15, places=1)
        self.assertAlmostEqual(self.lc.energy_range[1], 350, places=1)

    def test_filename(self):
        self.assertEqual(self.lc.filename, ones_file.name)

    def test_headers(self):
        self.assertEqual(self.lc.headers.num_headers, 4)

    def test_num_chans(self):
        self.assertEqual(self.lc.num_chans, 4)

    def test_time_range(self):
        t0, t1 = self.lc.time_range
        self.assertAlmostEqual(t0, 612354228.5, places=3)
        self.assertAlmostEqual(t1, 612355431.5, places=3)

    def test_trigtime(self):
        self.assertAlmostEqual(self.lc.trigtime, 612354468.864, places=3)

    def test_rebin_energy(self):
        lc2 = self.lc.rebin_energy(combine_by_factor, 2)
        self.assertEqual(lc2.num_chans, self.lc.num_chans//2)

    def test_rebin_time(self):
        lc2 = self.lc.rebin_time(combine_by_factor, 2)
        self.assertEqual(lc2.data.num_times,
                         self.lc.data.num_times//2)

    def test_slice_energy(self):
        lc2 = self.lc.slice_energy((50.0, 300.0))
        emin, emax = lc2.energy_range
        self.assertAlmostEqual(emin, 50, places=5)
        self.assertAlmostEqual(emax, 350, places=4)

    def test_slice_time(self):
        lc2 = self.lc.slice_time((612354238, 612354268))
        t0, t1 = lc2.time_range
        self.assertAlmostEqual(t0, 612354237.5, places=5)
        self.assertAlmostEqual(t1, 612354268.5, places=5)

    def test_to_lightcurve(self):
        lc2 = self.lc.to_lightcurve()
        self.assertEqual(self.lc.data.num_times, lc2.size)

    def test_to_pha(self):
        pha = self.lc.to_pha()
        self.assertEqual(self.lc.num_chans, pha.num_chans)

    def test_to_spectrum(self):
        spec = self.lc.to_spectrum()
        self.assertEqual(self.lc.num_chans, spec.size)

    def test_write(self):
        with TemporaryDirectory() as this_path:
            self.lc.write('.temp/')
            phaii = BatLightcurve.open(os.path.join('temp/', self.lc.filename))
            # self.assertListEqual(phaii.data.counts.tolist(), self.lc.data.counts.tolist())
            self.assertListEqual(phaii.data.tstart.tolist(), self.lc.data.tstart.tolist())
            self.assertListEqual(phaii.data.tstop.tolist(), self.lc.data.tstop.tolist())
            self.assertListEqual(phaii.data.exposure.tolist(), self.lc.data.exposure.tolist())
            self.assertListEqual(phaii.ebounds.low_edges(), self.lc.ebounds.low_edges())
            self.assertListEqual(phaii.ebounds.high_edges(), self.lc.ebounds.high_edges())
            self.assertListEqual(phaii.gti.low_edges(), self.lc.gti.low_edges())
            self.assertListEqual(phaii.gti.high_edges(), self.lc.gti.high_edges())
            self.assertEqual(phaii.trigtime, self.lc.trigtime)
            self.assertEqual(phaii.detector, self.lc.detector)
            self.assertEqual(phaii.headers[1], self.lc.headers[1])
            self.assertEqual(phaii.headers[2], self.lc.headers[2])
            self.assertEqual(phaii.headers[3], self.lc.headers[3])
            phaii.close()

@unittest.skipIf(not ms_file.exists(), "test files aren't downloaded. run gdt-download-data.")
class TestBatLightcurve2(unittest.TestCase):

    def setUp(self):
        self.lc = BatLightcurve.open(ms_file)

    def tearDown(self):
        self.lc.close()

    def test_energy_range(self):
        self.assertAlmostEqual(self.lc.energy_range[0], 15, places=1)
        self.assertAlmostEqual(self.lc.energy_range[1], 350, places=1)

    def test_filename(self):
        self.assertEqual(self.lc.filename, ms_file.name)

    def test_headers(self):
        self.assertEqual(self.lc.headers.num_headers, 4)

    def test_num_chans(self):
        self.assertEqual(self.lc.num_chans, 4)

    def test_time_range(self):
        t0, t1 = self.lc.time_range
        self.assertAlmostEqual(t0, 612354228.968, places=3)
        self.assertAlmostEqual(t1,  612355431.1439999, places=3)

    def test_trigtime(self):
        self.assertAlmostEqual(self.lc.trigtime, 612354468.864, places=3)

    def test_rebin_energy(self):
        lc2 = self.lc.rebin_energy(combine_by_factor, 2)
        self.assertEqual(lc2.num_chans, self.lc.num_chans//2)

    def test_rebin_time(self):
        lc2 = self.lc.rebin_time(combine_by_factor, 2)
        self.assertEqual(lc2.data.num_times,
                         self.lc.data.num_times//2)

    def test_slice_energy(self):
        lc2 = self.lc.slice_energy((50.0, 300.0))
        emin, emax = lc2.energy_range
        self.assertAlmostEqual(emin, 50, places=5)
        self.assertAlmostEqual(emax, 350, places=4)

    def test_slice_time(self):
        lc2 = self.lc.slice_time((612354238, 612354268))
        t0, t1 = lc2.time_range
        self.assertAlmostEqual(t0, 612354237.9920001, places=5)
        self.assertAlmostEqual(t1, 612354268.0079999, places=5)

    def test_to_lightcurve(self):
        lc2 = self.lc.to_lightcurve()
        self.assertEqual(self.lc.data.num_times, lc2.size)

    def test_to_pha(self):
        pha = self.lc.to_pha()
        self.assertEqual(self.lc.num_chans, pha.num_chans)

    def test_to_spectrum(self):
        spec = self.lc.to_spectrum()
        self.assertEqual(self.lc.num_chans, spec.size)

    def test_write(self):
        with TemporaryDirectory() as this_path:
            self.lc.write('temp/')
            phaii = BatLightcurve.open(os.path.join('temp/', self.lc.filename))
            #self.assertListEqual(phaii.data.counts.tolist(), self.lc.data.counts.tolist())
            self.assertListEqual(phaii.data.tstart.tolist(), self.lc.data.tstart.tolist())
            self.assertListEqual(phaii.data.tstop.tolist(), self.lc.data.tstop.tolist())
            self.assertListEqual(phaii.data.exposure.tolist(), self.lc.data.exposure.tolist())
            self.assertListEqual(phaii.ebounds.low_edges(), self.lc.ebounds.low_edges())
            self.assertListEqual(phaii.ebounds.high_edges(), self.lc.ebounds.high_edges())
            self.assertListEqual(phaii.gti.low_edges(), self.lc.gti.low_edges())
            self.assertListEqual(phaii.gti.high_edges(), self.lc.gti.high_edges())
            self.assertEqual(phaii.trigtime, self.lc.trigtime)
            self.assertEqual(phaii.detector, self.lc.detector)
            self.assertEqual(phaii.headers[1], self.lc.headers[1])
            self.assertEqual(phaii.headers[2], self.lc.headers[2])
            self.assertEqual(phaii.headers[3], self.lc.headers[3])
            phaii.close()
