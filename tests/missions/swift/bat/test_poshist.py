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
import numpy as np
from gdt.core import data_path
from gdt.core.coords import Quaternion
from gdt.missions.swift.bat.poshist import BatSao


@pytest.fixture
def test_file():
    print(data_path)
    return 'test_data/sw00974827000sao.fits'


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

        assert np.all(pos.obsgeoloc.xyz.value == np.array((-6165.602, -2728.5823, 1604.0405), dtype=np.float32))
        assert str(pos.obsgeoloc.xyz.unit) == 'm'

        assert np.all(pos.obsgeovel.xyz.value == np.array((3.400097, -6.4787993, 2.0060916), dtype=np.float32))
        assert str(pos.obsgeovel.xyz.unit) == 'm / s'

        # Let's verify the last row
        pos = frame[-1]
        assert pos.obstime.swift == 612355697.6006
        assert pos.quaternion == Quaternion((-0.2434614, 0.3955951, -0.5530058,
                                             0.691676))

        assert np.all(pos.obsgeoloc.xyz.value == np.array((6571.5796, -2167.505, 118.49594), dtype=np.float32))
        assert str(pos.obsgeoloc.xyz.unit) == 'm'

        assert np.all(pos.obsgeovel.xyz.value == np.array((2.2762816, 6.7394857, -2.6698375), dtype=np.float32))
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
