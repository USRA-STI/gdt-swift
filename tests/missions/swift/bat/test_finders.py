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
from gdt.missions.swift.bat.finders import *

download_dir = os.path.dirname(os.path.abspath(__file__))


class TestBatEventFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2020-05-28T10:28:00')
        obsid = '00974827000'
        cls.finder = BatEventFinder(t0, obsid)
    
    def test_cwd(self):
        assert self.finder.cwd == '/swift/data/obs/2020_05/00974827000/bat/event'
    
    def test_files(self):
        files = ['sw00974827000bevshsp_uf.evt.gz', 'sw00974827000bevtr.fits.gz']     
        for file in self.finder.files:
            assert file in files
    
    def test_num_files(self):
        assert self.finder.num_files == 2


class TestBatHousekeepingFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2020-05-28T10:28:00')
        obsid = '00974827000'
        cls.finder = BatHousekeepingFinder(t0, obsid)
    
    def test_cwd(self):
        assert self.finder.cwd == '/swift/data/obs/2020_05/00974827000/bat/hk'
    
    def test_files(self):
        files = ['sw00974827000bdecb.hk.gz', 'sw00974827000bdp.hk.gz', 
                 'sw00974827000bdqcb.hk.gz', 'sw00974827000ben.hk.gz',
                 'sw00974827000bevtlsp.hk.gz', 'sw00974827000bevtssp.hk.gz',
                 'sw00974827000bgocb.hk.gz', 'sw00974827000bhd.hk.gz']     
        for file in self.finder.files:
            assert file in files
    
    def test_num_files(self):
        assert self.finder.num_files == 8


class TestBatRateFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2020-05-28T10:28:00')
        obsid = '00974827000'
        cls.finder = BatRateFinder(t0, obsid)
    
    def test_cwd(self):
        assert self.finder.cwd == '/swift/data/obs/2020_05/00974827000/bat/rate'
    
    def test_files(self):
        files = ['sw00974827000brt1s.lc.gz', 'sw00974827000brtmc.lc.gz',
                 'sw00974827000brtms.lc.gz', 'sw00974827000brtqd.lc.gz']     
        for file in self.finder.files:
            assert file in files
    
    def test_num_files(self):
        assert self.finder.num_files == 4


class TestBatSurveyFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2020-05-28T10:28:00')
        obsid = '00974827000'
        cls.finder = BatSurveyFinder(t0, obsid)
    
    def test_cwd(self):
        assert self.finder.cwd == '/swift/data/obs/2020_05/00974827000/bat/survey'
    
    def test_files(self):
        files = ['sw00974827000bsvabo0e78g030f.dph.gz',
                 'sw00974827000bsvabo0e78g0310.dph.gz',
                 'sw00974827000bsvpbo0e78g030f.dph.gz']     
        for file in self.finder.files:
            assert file in files
    
    def test_num_files(self):
        assert self.finder.num_files == 3


class TestBatTriggerFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2020-05-28T10:28:00')
        obsid = '00974827000'
        cls.finder = BatTriggerFinder(t0, obsid)
    
    def test_cwd(self):
        assert self.finder.cwd == '/swift/data/obs/2020_05/00974827000/bat/products'
    
    def test_files(self):
        files = ['sw00974827000bev1s.lc.gz', 'sw00974827000bev1s_lc.gif',
                 'sw00974827000bev_skim.gif', 'sw00974827000bevas.pha.gz',
                 'sw00974827000bevas.rsp.gz', 'sw00974827000bevas_dt.img.gz',
                 'sw00974827000bevas_sk.img.gz', 'sw00974827000bevbu.gti.gz',
                 'sw00974827000bevms.lc.gz', 'sw00974827000bevpb_dt.img.gz',
                 'sw00974827000bevpb_sk.img.gz', 'sw00974827000bevps.pha.gz',
                 'sw00974827000bevps.rsp.gz', 'sw00974827000bevps_dt.img.gz',
                 'sw00974827000bevps_sk.img.gz', 'sw00974827000bevsl.pha.gz']
                      
        for file in self.finder.files:
            assert file in files
    
    def test_num_files(self):
        assert self.finder.num_files == 16


class TestBatEventTemporalFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2020-05-28T10:28:00')
        t1 = Time('2020-05-28T11:28:00')
        cls.finder = BatEventTemporalFinder(t0, tstop=t1)
    
    def test_cwd(self):
        dirs = ['/swift/data/obs/2020_05/00974827000/bat/event']
        for dir in self.finder.cwd:
            assert dir in dirs
        
        assert len(self.finder.cwd) == 1

    def test_num_files(self):
        assert self.finder.num_files == 2

    def test_ls_event(self):
        files = ['sw00974827000bevshsp_uf.evt.gz']
                 
        event_files = self.finder.ls_event()
        assert len(event_files) == 1
        for file in event_files:
            assert file in files
    
    @unittest.skip('Large Download')
    def test_get_event(self):
        filepaths = self.finder.get_event(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)


class TestBatHousekeepingTemporalFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2020-05-28T10:28:00')
        t1 = Time('2020-05-28T11:28:00')
        cls.finder = BatHousekeepingTemporalFinder(t0, tstop=t1)
    
    def test_cwd(self):
        dirs = ['/swift/data/obs/2020_05/00013483015/bat/hk',
                '/swift/data/obs/2020_05/03106436001/bat/hk',
                '/swift/data/obs/2020_05/00095119034/bat/hk',
                '/swift/data/obs/2020_05/00974827000/bat/hk']
                
        for dir in self.finder.cwd:
            assert dir in dirs
        
        assert len(self.finder.cwd) == 4

    def test_num_files(self):
        assert self.finder.num_files == 22
    
    def test_ls_det_enabled(self):
        files = ['sw00013483015bdecb.hk.gz', 'sw03106436001bdecb.hk.gz', 
                 'sw00095119034bdecb.hk.gz', 'sw00974827000bdecb.hk.gz']
                 
        det_enabled_files = self.finder.ls_det_enabled()
        assert len(det_enabled_files) == 4
        for file in det_enabled_files:
            assert file in files

    def test_ls_gain_offset(self):
        files = ['sw00013483015bgocb.hk.gz', 'sw03106436001bgocb.hk.gz', 
                 'sw00095119034bgocb.hk.gz', 'sw00974827000bgocb.hk.gz']
                 
        gain_offset_files = self.finder.ls_gain_offset()
        assert len(gain_offset_files) == 4
        for file in gain_offset_files:
            assert file in files
    
    def test_get_det_enabled(self):
        filepaths = self.finder.get_det_enabled(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

    def test_get_gain_offset(self):
        filepaths = self.finder.get_gain_offset(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)


class TestBatRateTemporalFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2020-05-28T10:28:00')
        t1 = Time('2020-05-28T11:28:00')
        cls.finder = BatRateTemporalFinder(t0, tstop=t1)
    
    def test_cwd(self):
        dirs = ['/swift/data/obs/2020_05/00013483015/bat/rate',
                '/swift/data/obs/2020_05/03106436001/bat/rate',
                '/swift/data/obs/2020_05/00095119034/bat/rate',
                '/swift/data/obs/2020_05/00974827000/bat/rate']
                
        for dir in self.finder.cwd:
            assert dir in dirs
        
        assert len(self.finder.cwd) == 4

    def test_num_files(self):
        # 4 folders, 4 files each
        assert self.finder.num_files == 16
    
    def test_ls_millisecond_lc(self):
        files = ['sw00013483015brtms.lc.gz', 'sw03106436001brtms.lc.gz', 
                 'sw00095119034brtms.lc.gz', 'sw00974827000brtms.lc.gz']
                 
        ms_lc_files = self.finder.ls_millisecond_lc()
        assert len(ms_lc_files) == 4
        for file in ms_lc_files:
            assert file in files

    def test_ls_multichannel_lc(self):
        files = ['sw00013483015brtmc.lc.gz', 'sw03106436001brtmc.lc.gz', 
                 'sw00095119034brtmc.lc.gz', 'sw00974827000brtmc.lc.gz']
                 
        multi_lc_files = self.finder.ls_multichannel_lc()
        assert len(multi_lc_files) == 4
        for file in multi_lc_files:
            assert file in files

    def test_ls_quadrant_lc(self):
        files = ['sw00013483015brtqd.lc.gz', 'sw03106436001brtqd.lc.gz', 
                 'sw00095119034brtqd.lc.gz', 'sw00974827000brtqd.lc.gz']
                 
        quad_lc_files = self.finder.ls_quadrant_lc()
        assert len(quad_lc_files) == 4
        for file in quad_lc_files:
            assert file in files

    def test_ls_second_lc(self):
        files = ['sw00013483015brt1s.lc.gz', 'sw03106436001brt1s.lc.gz', 
                 'sw00095119034brt1s.lc.gz', 'sw00974827000brt1s.lc.gz']
                 
        sec_lc_files = self.finder.ls_second_lc()
        assert len(sec_lc_files) == 4
        for file in sec_lc_files:
            assert file in files

    def test_get_millisecond_lc(self):
        filepaths = self.finder.get_millisecond_lc(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

    def test_get_multichannel_lc(self):
        filepaths = self.finder.get_multichannel_lc(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

    def test_get_quadrant_lc(self):
        filepaths = self.finder.get_quadrant_lc(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

    def test_get_second_lc(self):
        filepaths = self.finder.get_second_lc(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)


class TestBatSurveyTemporalFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2020-05-28T10:28:00')
        t1 = Time('2020-05-28T11:28:00')
        cls.finder = BatSurveyTemporalFinder(t0, tstop=t1)
    
    def test_cwd(self):
        dirs = ['/swift/data/obs/2020_05/00013483015/bat/survey',
                '/swift/data/obs/2020_05/03106436001/bat/survey',
                '/swift/data/obs/2020_05/00095119034/bat/survey',
                '/swift/data/obs/2020_05/00974827000/bat/survey']
                
        for dir in self.finder.cwd:
            assert dir in dirs
        
        assert len(self.finder.cwd) == 4

    def test_num_files(self):
        assert self.finder.num_files == 11

    def test_ls_survey(self):
        files = ['sw00013483015bsvpbo0e6ag030d.dph.gz', 
                 'sw00013483015bsvpbo0e6fg030e.dph.gz', 
                 'sw00013483015bsvpbo0e73g030e.dph.gz', 
                 'sw00013483015bsvpbo0e75g030f.dph.gz', 
                 'sw00013483015bsvpbo0e77g030f.dph.gz', 
                 'sw03106436001bsvpbo0e6eg030d.dph.gz', 
                 'sw03106436001bsvpbo0e77g030f.dph.gz', 
                 'sw00095119034bsvpbo0e78g030f.dph.gz', 
                 'sw00974827000bsvabo0e78g030f.dph.gz', 
                 'sw00974827000bsvabo0e78g0310.dph.gz', 
                 'sw00974827000bsvpbo0e78g030f.dph.gz']
                 
        survey_files = self.finder.ls_survey()
        assert len(survey_files) == 11
        for file in survey_files:
            assert file in files
    
    def test_get_survey(self):
        filepaths = self.finder.get_survey(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)


class TestBatTriggerTemporalFinder(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        t0 = Time('2020-05-28T10:28:00')
        t1 = Time('2020-05-28T11:28:00')
        cls.finder = BatTriggerTemporalFinder(t0, tstop=t1)
    
    def test_cwd(self):
        dirs = ['/swift/data/obs/2020_05/00974827000/bat/products']
        for dir in self.finder.cwd:
            assert dir in dirs
        
        assert len(self.finder.cwd) == 1

    def test_num_files(self):
        assert self.finder.num_files == 16

    def test_ls_afterslew(self):
        files = ['sw00974827000bevas.pha.gz', 'sw00974827000bevas.rsp.gz', 
                'sw00974827000bevas_dt.img.gz', 'sw00974827000bevas_sk.img.gz']
                 
        as_files = self.finder.ls_afterslew()
        assert len(as_files) == 4
        for file in as_files:
            assert file in files

    def test_ls_gti(self):
        files = ['sw00974827000bevbu.gti.gz']
                 
        gti_files = self.finder.ls_gti()
        assert len(gti_files) == 1
        for file in gti_files:
            assert file in files
    
    def test_ls_lightcurve(self):
        files = ['sw00974827000bev1s.lc.gz', 'sw00974827000bevms.lc.gz']
                 
        lc_files = self.finder.ls_lightcurve()
        assert len(lc_files) == 2
        for file in lc_files:
            assert file in files

    def test_ls_peak(self):
        files = ['sw00974827000bevpb_dt.img.gz', 'sw00974827000bevpb_sk.img.gz']
                 
        peak_files = self.finder.ls_peak()
        assert len(peak_files) == 2
        for file in peak_files:
            assert file in files

    def test_ls_preslew(self):
        files = ['sw00974827000bevpb_dt.img.gz', 'sw00974827000bevpb_sk.img.gz']
                 
        ps_files = self.finder.ls_preslew()
        assert len(ps_files) == 2
        for file in ps_files:
            assert file in files

    def test_ls_quicklook(self):
        files = ['sw00974827000bev1s_lc.gif', 'sw00974827000bev_skim.gif']
                 
        q_files = self.finder.ls_quicklook()
        assert len(q_files) == 2
        for file in q_files:
            assert file in files

    def test_ls_slew(self):
        files = ['sw00974827000bevsl.pha.gz']
                 
        s_files = self.finder.ls_slew()
        assert len(s_files) == 1
        for file in s_files:
            assert file in files
    
    def test_get_afterslew(self):
        filepaths = self.finder.get_afterslew(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

    def test_get_gti(self):
        filepaths = self.finder.get_gti(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

    def test_get_lightcurve(self):
        filepaths = self.finder.get_lightcurve(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

    def test_get_peak(self):
        filepaths = self.finder.get_peak(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

    def test_get_preslew(self):
        filepaths = self.finder.get_preslew(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

    def test_get_quicklook(self):
        filepaths = self.finder.get_quicklook(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

    def test_get_slew(self):
        filepaths = self.finder.get_slew(download_dir)
        for filepath in filepaths:
            assert os.path.exists(filepath)
            os.remove(filepath)

