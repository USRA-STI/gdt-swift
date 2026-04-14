#  CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT WITH UNLIMITED RIGHTS
#
#  Contract No.: CA 80MSFC17M0022
#  Contractor Name: Universities Space Research Association
#  Contractor Address: 7178 Columbia Gateway Drive, Columbia, MD 21046
#
#  Copyright 2017-2022 by Universities Space Research Association (USRA). All rights reserved.
#
#  Developed by: William Cleveland and Adam Goldstein
#                Universities Space Research Association
#                Science and Technology Institute
#                https://sti.usra.edu
#
#  Developed by: Daniel Kocevski
#                National Aeronautics and Space Administration (NASA)
#                Marshall Space Flight Center
#                Astrophysics Branch (ST-12)
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
#   in compliance with the License. You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License
#  is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#  implied. See the License for the specific language governing permissions and limitations under the
#  License.
#
import unittest
import numpy as np
from astropy.time import Time
from gdt.core.coords import Quaternion
from gdt.core.coords.spacecraft import SpacecraftFrame
from gdt.core.healpix import HealPixLocalization
from gdt.missions.swift.bat.detectors import HealPixPartialCoding, BatPartialCoding



class TestHealPixPartialCoding(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # create a partial coding test from a 10-deg gaussian
        hpx = HealPixLocalization.from_gaussian(30.0, 30.0, 10.0)
        cls.hpx_arr = hpx.prob / hpx.prob.max()
        cls.hpx = HealPixPartialCoding.from_data(cls.hpx_arr)
    
    def test_pcoding(self):
        assert np.all(self.hpx.pcoding == self.hpx_arr)
    
    def test_area(self):
        # 10-deg gaussian has a 1-sigma that encloses ~314 deg^2
        # 1 sigma in 2D encloses ~39.3% of the probability.
        # therefore, this should be ~equivalent to a partial coding of 
        # 1-0.393. Check to make sure we are within 1% of this.
    
        assert abs( (self.hpx.area(1.0 - 0.393) - 314.0) / 314.0 ) < 0.01
    
    def test_partial_coding(self):
        # partial coding should be ~1 at center
        assert self.hpx.partial_coding(30.0, 30.0) > 0.99
        
        # partial coding should be ~0 far away
        assert self.hpx.partial_coding(150.0, -30.0) < 1e-6
    
    def test_partial_coding_path(self):
        path = self.hpx.partial_coding_path(0.95)
        # this path should be continuous; only one complete closed segment
        assert len(path) == 1
        # all points in the path should be within a few degrees of (30., 30.)
        assert np.all( np.abs(path[0] - 30.0) < 5.0 )
    
    def test_rotate(self):
        # rotation from (30.0, 30.0) to ~(180.0, 0.0)
        quat = [0.0, -0.7071, 0.6124, 0.3536]
        frame = SpacecraftFrame(obstime = Time.now(),
                          quaternion=Quaternion(quat))
        
        hpx_rot = self.hpx.rotate(frame)
        # peak partial coding should now be at ~(180.0, 0.0)
        assert hpx_rot.partial_coding(180.0, 0.0) > 0.99
        assert hpx_rot.partial_coding(30.0, 30.0) < 1e-6


class TestBatPartialCoding(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.bat = BatPartialCoding()
    
    def test_nside(self):
        assert self.bat.nside == 128
    
    def test_partial_coding(self):
        assert self.bat.partial_coding(0.0, 0.0) == 1.0
        assert self.bat.partial_coding(0.0, 90.0) == 0.0
    
    def test_rotate(self):
        # the first quaternion contained in sw00974827000sao.fits.gz
        quat = [-0.35197902, -0.34436679, -0.75078022,  0.44028553]
        frame = SpacecraftFrame(obstime = Time.now(),
                          quaternion=Quaternion(quat))
        
        bat_rot = self.bat.rotate(frame)
        # the corresponding RA/Dec pointing from that file is 228.95697, 56.27967
        assert bat_rot.partial_coding(228.95697, 56.27967) == 1.0
        assert bat_rot.partial_coding(0.0, 0.0) == 0.0
        
