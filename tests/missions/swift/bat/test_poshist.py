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
import pytest
import unittest
import numpy as np
from tempfile import TemporaryDirectory
from gdt.core import data_path
from gdt.core.coords import Quaternion
from gdt.missions.swift.bat.poshist import BatSao


@pytest.fixture
def test_file():
    return data_path / 'swift-bat' / 'sw00974827000sao.fits.gz'

def test_get_spacecraft_frame(test_file):
    # if not test_file.exists():
    #     pytest.skip("test files aren't downloaded. run gdt-download-data.")

    with BatSao.open(test_file) as poshist:
        frame = poshist.get_spacecraft_frame()
        # This file has 2162 rows
        assert frame.obstime.size == 2162

        # Let's verify the first row
        pos = frame[0]
        assert pos.obstime.swift == 612353536.6006
        assert pos.quaternion == Quaternion((-0.351979, -0.3443668, -0.7507802,
                                             0.4402855))
        
        assert round(pos.obsgeoloc.x.value, 1) == round(np.float32(-6165602.0), 1)
        assert round(pos.obsgeoloc.y.value, 1) == round(np.float32(-2728582.2), 1)
        assert round(pos.obsgeoloc.z.value, 1) == round(np.float32(1604040.5), 1)
        assert str(pos.obsgeoloc.xyz.unit) == 'm'

        assert round(pos.obsgeovel.x.value, 3) == round(np.float32(3400.097), 3)
        assert round(pos.obsgeovel.y.value, 3) == round(np.float32(-6478.7993), 3)
        assert round(pos.obsgeovel.z.value, 3) == round(np.float32(2006.0916), 3)
        assert str(pos.obsgeovel.xyz.unit) == 'm / s'

        # Let's verify the last row
        pos = frame[-1]
        assert pos.obstime.swift == 612355697.6006
        assert pos.quaternion == Quaternion((-0.2434614, 0.3955951, -0.5530058,
                                             0.691676))

        assert round(pos.obsgeoloc.x.value, 1) == round(np.float32(6571579.6), 1)
        assert round(pos.obsgeoloc.y.value, 1) == round(np.float32(-2167505.0), 1)
        assert round(pos.obsgeoloc.z.value, 1) == round(np.float32(118495.9), 1)
        assert str(pos.obsgeoloc.xyz.unit) == 'm'

        assert round(pos.obsgeovel.x.value, 3) == round(np.float32(2276.2816), 3)
        assert round(pos.obsgeovel.y.value, 3) == round(np.float32(6739.4857), 3)
        assert round(pos.obsgeovel.z.value, 3) == round(np.float32(-2669.8375), 3)
        assert str(pos.obsgeovel.xyz.unit) == 'm / s'


def test_get_spacecraft_states(test_file):
    # if not test_file.exists():
    #     pytest.skip("test files aren't downloaded. run gdt-download-data.")

    with BatSao.open(test_file) as poshist:
        states = poshist.get_spacecraft_states()
        # This file has 86520 rows
        assert len(states) == 2162

        # First row
        # Value of flag = 1 which means "in sun" and "not in SAA"
        state = states[0]
        assert state['saa'] == False
        assert state['sun'] == False

        # Last row
        # Value of flag = 1 which means "in sun" and "not in SAA"
        state = states[-1]
        assert state['saa'] == False
        assert state['sun'] == True

        # Row 3683
        # Value of flag = 0 which means "not in sun" and "not in SAA"
        state = states[1182]
        assert state['saa'] == False
        assert state['sun'] == False
