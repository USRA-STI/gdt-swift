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

from gdt.missions.swift.time import *
from gdt.missions.swift.finders import *

download_dir = os.path.dirname(os.path.abspath(__file__))


class TestSwiftObsFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2025-12-01T12:00:00')
        obsid = '00098298003'
        cls.finder = SwiftObsFinder(t0, obsid)
    
    def test_files(self):
        folders = ['auxil', 'bat', 'log', 'uvot', 'xrt']
        for file in self.finder.files:
            assert file in folders
    
    def test_num_files(self):
        assert self.finder.num_files == 5


class TestSwiftTemporalFinderTstart(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2025-12-01T12:00:00')
        cls.finder = SwiftTemporalFinder(t0)
    
    def test_cwd(self):
        dirs = ['/swift/data/obs/2025_11/03112638005',
                '/swift/data/obs/2025_11/00097408004',
                '/swift/data/obs/2025_11/00092103033',
                '/swift/data/obs/2025_12/00016862002',
                '/swift/data/obs/2025_12/00098052012',
                '/swift/data/obs/2025_12/00032613226',
                '/swift/data/obs/2025_12/00098298003',
                '/swift/data/obs/2025_12/00045958010',
                '/swift/data/obs/2025_12/00074220027',
                '/swift/data/obs/2025_12/00097889004',
                '/swift/data/obs/2025_12/00097905006',
                '/swift/data/obs/2025_12/00090560007']
        
        for dir in self.finder.cwd:
            assert dir in dirs

    def test_files(self):
        folders = ['auxil', 'bat', 'log', 'uvot', 'xrt']
        for file in self.finder.files:
            assert file in folders
        
    def test_num_files(self):
        # 5 files per directory, 12 directories
        assert self.finder.num_files == 12 * 5
    
    def test_filter(self):
        filtered_files = self.finder.filter('auxil', '')
        assert len(filtered_files) == 12
        for file in filtered_files:
            assert file == 'auxil'


class TestSwiftTemporalFinderTstartTstop(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2025-12-01T12:00:00')
        t1 = Time('2025-12-01T14:00:00')
        cls.finder = SwiftTemporalFinder(t0, tstop=t1)
    
    def test_cwd(self):
        dirs = ['/swift/data/obs/2025_11/00092103033',
                '/swift/data/obs/2025_12/00032613226',
                '/swift/data/obs/2025_12/00097905006',
                '/swift/data/obs/2025_12/00090560007']
        
        for dir in self.finder.cwd:
            assert dir in dirs
    
    def test_files(self): 
        folders = ['auxil', 'bat', 'log', 'uvot', 'xrt']
        for file in self.finder.files:
            assert file in folders

    def test_num_files(self):
        # 5 files per directory, 4 directories
        assert self.finder.num_files == 5 * 4


class TestSwiftAuxilFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2025-12-01T12:00:00')
        obsid = '00098298003'
        cls.finder = SwiftAuxilFinder(t0, obsid)
    
    def test_cwd(self):
        assert self.finder.cwd == '/swift/data/obs/2025_12/00098298003/auxil'
    
    def test_files(self):
        files = ['SWIFT_TLE_ARCHIVE.txt.25344.16528503.gz',
                 'sw00098298003pat.fits.gz',
                 'sw00098298003pjb.par.gz',
                 'sw00098298003pob.cat.gz',
                 'sw00098298003ppr.par.gz',
                 'sw00098298003s.mkf.gz',
                 'sw00098298003sao.fits.gz',
                 'sw00098298003sat.fits.gz',
                 'sw00098298003sen.hk.gz',
                 'sw00098298003sti.fits.gz',
                 'sw00098298003uat.fits.gz',
                 'sw00098298003x.mkf.gz']
        
        for file in self.finder.files:
            assert file in file
    
    def test_num_files(self):
        assert self.finder.num_files == 12


class TestSwiftAuxilTemporalFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2025-12-01T12:00:00')
        t1 = Time('2025-12-01T14:00:00')
        cls.finder = SwiftAuxilTemporalFinder(t0, tstop=t1)
    
    def test_cwd(self):
        dirs = ['/swift/data/obs/2025_11/00092103033/auxil',
                '/swift/data/obs/2025_12/00032613226/auxil',
                '/swift/data/obs/2025_12/00097905006/auxil',
                '/swift/data/obs/2025_12/00090560007/auxil']
        
        for dir in self.finder.cwd:
            assert dir in dirs
        
        assert len(self.finder.cwd) == 4

    def test_num_files(self):
        # 12 files per directory, 4 directories
        assert self.finder.num_files == 12 * 4

    def test_ls_orbit(self):
        files = ['sw00092103033sao.fits.gz', 
                 'sw00032613226sao.fits.gz', 
                 'sw00097905006sao.fits.gz', 
                 'sw00090560007sao.fits.gz']
                 
        orbit_files = self.finder.ls_orbit()
        assert len(orbit_files) == 4
        for file in orbit_files:
            assert file in files
    
    def test_ls_attitude(self):
        pat_files = ['sw00092103033pat.fits.gz', 'sw00032613226pat.fits.gz', 
                     'sw00097905006pat.fits.gz', 'sw00090560007pat.fits.gz']
        sat_files = ['sw00092103033sat.fits.gz', 'sw00032613226sat.fits.gz', 
                     'sw00097905006sat.fits.gz', 'sw00090560007sat.fits.gz']
        uat_files = ['sw00092103033uat.fits.gz', 'sw00032613226uat.fits.gz', 
                     'sw00097905006uat.fits.gz', 'sw00090560007uat.fits.gz']
        all_files = pat_files + sat_files + uat_files
        
        files = self.finder.ls_attitude(which='pat')
        assert len(files) == 4
        for file in files:
            assert file in pat_files

        files = self.finder.ls_attitude(which='sat')
        assert len(files) == 4
        for file in files:
            assert file in sat_files

        files = self.finder.ls_attitude(which='uat')
        assert len(files) == 4
        for file in files:
            assert file in uat_files

        files = self.finder.ls_attitude(which='best')
        assert len(files) == 4
        for file in files:
            assert file in uat_files

        files = self.finder.ls_attitude(which='all')
        assert len(files) == 12
        for file in files:
            assert file in all_files
    
    def test_get_orbit(self):
        filepaths = self.finder.get_orbit(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

    def test_get_attitude(self):
        filepaths = self.finder.get_attitude(download_dir, which='best')
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)
