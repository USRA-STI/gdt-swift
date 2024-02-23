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

from gdt.missions.swift.time import *
from gdt.missions.swift.bat.finders import *

download_dir = os.path.dirname(os.path.abspath(__file__))


class TestBatDataProductsFtp(unittest.TestCase):

    def setUp(self):
        self.finder = BatDataProductsFtp('00974827', '2020-05')

    def test_set_cd(self):
        #self.finder.cd()
        self.assertEqual(self.finder.num_files, 14)


    def test_ls(self):
        # self.finder.cd()
        [self.assertTrue('gti' in file) for file in self.finder.ls_gti()]
        [self.assertTrue('lc' in file) for file in self.finder.ls_lightcurve()]
        [self.assertTrue('rsp' in file) for file in self.finder.ls_response()]
        [self.assertTrue('pha' in file) for file in self.finder.ls_pha()]
        [self.assertTrue('bevps' in file) for file in self.finder.ls_preslew()]
        [self.assertTrue('bevsl' in file) for file in self.finder.ls_slew()]
        [self.assertTrue('bevas' in file) for file in self.finder.ls_afterslew()]

    def test_get(self):

        self.finder.get_gti(download_dir)
        self.finder.get_lightcurve(download_dir)
        self.finder.get_response(download_dir)
        self.finder.get_pha(download_dir)
        self.finder.get_preslew(download_dir)
        self.finder.get_slew(download_dir)
        self.finder.get_afterslew(download_dir)

        files = self.finder.ls_lightcurve()
        files.extend(self.finder.ls_lightcurve())
        for file in files:
            try:
                os.remove(os.path.join(download_dir, file))
            except:
                pass

class TestBatAuxiliaryFtp(unittest.TestCase):

    def setUp(self):
        self.finder = BatAuxiliaryFtp('00974827', '2020-05')

    def test_set_cd(self):
        #self.finder.cd()
        self.assertEqual(self.finder.num_files, 12)

    def test_ls(self):

        [self.assertTrue('sao' in file) for file in self.finder.ls_sao()]
        [self.assertTrue('sat' in file) for file in self.finder.ls_sat()]


    def test_get(self):

        self.finder.get_sao(download_dir)
        self.finder.get_sat(download_dir)

        files = self.finder.ls_sat()
        files.extend(self.finder.ls_sat())
        for file in files:
            try:
                os.remove(os.path.join(download_dir, file))
            except:
                pass
