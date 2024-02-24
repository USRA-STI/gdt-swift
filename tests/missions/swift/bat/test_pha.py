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
from pathlib import Path
from gdt.core import data_path
from gdt.missions.swift.bat.pha import *
from gdt.core.binning.binned import combine_by_factor


ps_file = data_path / 'swift-bat' / 'sw00974827000bevps.pha.gz'
as_file = data_path / 'swift-bat' /'sw00974827000bevas.pha.gz'
sl_file = data_path / 'swift-bat' /'sw00974827000bevsl.pha.gz'


@unittest.skipIf(not ps_file.exists(), "test files aren't downloaded. run gdt-download-data.")
class TestBatPha_Ps(unittest.TestCase):

    def setUp(self):
        self.pha = BatPha.open(ps_file)

    def tearDown(self):
        self.pha.close()

    def test_energy_range(self):
        self.assertAlmostEqual(self.pha.energy_range[0], 0.0, places=1)
        self.assertAlmostEqual(self.pha.energy_range[1], 6553.6, places=1)

    def test_filename(self):
        self.assertEqual(self.pha.filename, ps_file.name)

    def test_headers(self):
        self.assertEqual(self.pha.headers.num_headers, 4)

    def test_num_chans(self):
        self.assertEqual(self.pha.num_chans, 80)

    def test_time_range(self):
        t0, t1 = self.pha.time_range
        t0 += self.pha.trigtime
        t1 += self.pha.trigtime
        self.assertAlmostEqual(t0,  612354468.276, places=3)
        self.assertAlmostEqual(t1, 612354479.4006, places=3)

    def test_trigtime(self):
        self.assertAlmostEqual(self.pha.trigtime, 612354468.864, places=3)

    def test_rebin_energy(self):
        pha2 = self.pha.rebin_energy(combine_by_factor, 2)
        self.assertEqual(pha2.num_chans, self.pha.num_chans//2)

    def test_slice_energy(self):
        pha2 = self.pha.slice_energy((50.0, 100.0))
        emin, emax = pha2.energy_range
        self.assertAlmostEqual(emin, 48.9, places=1)
        self.assertAlmostEqual(emax, 101.2, places=1)

    def test_write(self):
        with TemporaryDirectory() as this_path:
            self.pha.write(this_path, overwrite=True)
            pha = BatPha.open(os.path.join(this_path, self.pha.filename))
            self.assertListEqual(pha.data.counts.tolist(), self.pha.data.counts.tolist())
            self.assertListEqual(pha.data.exposure.tolist(), self.pha.data.exposure.tolist())
            self.assertListEqual(pha.ebounds.low_edges(), self.pha.ebounds.low_edges())
            self.assertListEqual(pha.ebounds.high_edges(), self.pha.ebounds.high_edges())
            self.assertListEqual(pha.gti.low_edges(), self.pha.gti.low_edges())
            self.assertListEqual(pha.gti.high_edges(), self.pha.gti.high_edges())
            self.assertEqual(pha.trigtime, self.pha.trigtime)
            try:
                self.assertEqual(pha.headers[1], self.pha.headers[1])
                self.assertEqual(pha.headers[2], self.pha.headers[2])
                self.assertEqual(pha.headers[3], self.pha.headers[3])
            except AssertionError:
                    pass
            pha.close()

@unittest.skipIf(not as_file.exists(), "test files aren't downloaded. run gdt-download-data.")
class TestBatPha_As(unittest.TestCase):

    def setUp(self):
        self.pha = BatPha.open(as_file)

    def tearDown(self):
        self.pha.close()

    def test_energy_range(self):
        self.assertAlmostEqual(self.pha.energy_range[0], 0.0, places=1)
        self.assertAlmostEqual(self.pha.energy_range[1], 6553.6, places=1)

    def test_filename(self):
        self.assertEqual(self.pha.filename, as_file.name)

    def test_headers(self):
        self.assertEqual(self.pha.headers.num_headers, 4)

    def test_num_chans(self):
        self.assertEqual(self.pha.num_chans, 80)

    def test_time_range(self):
        t0, t1 = self.pha.time_range
        t0 += self.pha.trigtime
        t1 += self.pha.trigtime
        self.assertAlmostEqual(t0, 612354538.60058, places=3)
        self.assertAlmostEqual(t1,  612354582.068, places=3)

    def test_trigtime(self):
        self.assertAlmostEqual(self.pha.trigtime, 612354468.864, places=3)

    def test_rebin_energy(self):
        pha2 = self.pha.rebin_energy(combine_by_factor, 2)
        self.assertEqual(pha2.num_chans, self.pha.num_chans//2)

    def test_slice_energy(self):
        pha2 = self.pha.slice_energy((50.0, 100.0))
        emin, emax = pha2.energy_range
        self.assertAlmostEqual(emin, 48.9, places=1)
        self.assertAlmostEqual(emax, 101.2, places=1)

    def test_write(self):
        with TemporaryDirectory() as this_path:
            self.pha.write(this_path, overwrite=True)
            pha = BatPha.open(os.path.join(this_path, self.pha.filename))
            self.assertListEqual(pha.data.counts.tolist(), self.pha.data.counts.tolist())
            self.assertListEqual(pha.data.exposure.tolist(), self.pha.data.exposure.tolist())
            self.assertListEqual(pha.ebounds.low_edges(), self.pha.ebounds.low_edges())
            self.assertListEqual(pha.ebounds.high_edges(), self.pha.ebounds.high_edges())
            self.assertListEqual(pha.gti.low_edges(), self.pha.gti.low_edges())
            self.assertListEqual(pha.gti.high_edges(), self.pha.gti.high_edges())
            self.assertEqual(pha.trigtime, self.pha.trigtime)
            try:
                self.assertEqual(pha.headers[1], self.pha.headers[1])
                self.assertEqual(pha.headers[2], self.pha.headers[2])
                self.assertEqual(pha.headers[3], self.pha.headers[3])
            except AssertionError:
                    pass
            pha.close()

@unittest.skipIf(not sl_file.exists(), "test files aren't downloaded. run gdt-download-data.")
class TestBatPha_Sl(unittest.TestCase):

    def setUp(self):
        self.pha = BatPha.open(sl_file)

    def tearDown(self):
        self.pha.close()

    def test_energy_range(self):
        self.assertAlmostEqual(self.pha.energy_range[0], 0.0, places=1)
        self.assertAlmostEqual(self.pha.energy_range[1], 6553.6, places=1)

    def test_filename(self):
        self.assertEqual(self.pha.filename, sl_file.name)

    def test_headers(self):
        self.assertEqual(self.pha.headers.num_headers, 4)

    def test_num_chans(self):
        self.assertEqual(self.pha.num_chans, 80)

    def test_time_range(self):
        t0, t1 = self.pha.time_range
        t0 += self.pha.trigtime
        t1 += self.pha.trigtime
        self.assertAlmostEqual(t0, 612354479.4006, places=3)
        self.assertAlmostEqual(t1,  612354538.60058, places=3)

    def test_trigtime(self):
        self.assertAlmostEqual(self.pha.trigtime, 612354468.864, places=3)

    def test_rebin_energy(self):
        pha2 = self.pha.rebin_energy(combine_by_factor, 2)
        self.assertEqual(pha2.num_chans, self.pha.num_chans//2)

    def test_slice_energy(self):
        pha2 = self.pha.slice_energy((50.0, 100.0))
        emin, emax = pha2.energy_range
        self.assertAlmostEqual(emin, 48.9, places=1)
        self.assertAlmostEqual(emax, 101.2, places=1)

    def test_write(self):
        with TemporaryDirectory() as this_path:
            self.pha.write(this_path, overwrite=True)
            pha = BatPha.open(os.path.join(this_path, self.pha.filename))
            self.assertListEqual(pha.data.counts.tolist(), self.pha.data.counts.tolist())
            self.assertListEqual(pha.data.exposure.tolist(), self.pha.data.exposure.tolist())
            self.assertListEqual(pha.ebounds.low_edges(), self.pha.ebounds.low_edges())
            self.assertListEqual(pha.ebounds.high_edges(), self.pha.ebounds.high_edges())
            self.assertListEqual(pha.gti.low_edges(), self.pha.gti.low_edges())
            self.assertListEqual(pha.gti.high_edges(), self.pha.gti.high_edges())
            self.assertEqual(pha.trigtime, self.pha.trigtime)
            try:
                self.assertEqual(pha.headers[1], self.pha.headers[1])
                self.assertEqual(pha.headers[2], self.pha.headers[2])
                self.assertEqual(pha.headers[3], self.pha.headers[3])
            except AssertionError:
                    pass
            pha.close()
