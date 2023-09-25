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
import numpy as np
import astropy.units as u
from astropy.timeseries import TimeSeries
import astropy.coordinates.representation as r
from gdt.core.coords import Quaternion
from gdt.core.file import FitsFileContextManager
from gdt.core.coords.spacecraft import SpacecraftFrameModelMixin, SpacecraftStatesModelMixin
from gdt.core.coords.spacecraft import SpacecraftFrame
from gdt.missions.swift.time import Time
from gdt.missions.swift.bat.headers import SaoHeaders
#from .detectors import GbmDetectors



_all__ = ['BatSao']

SWIFT_TO_UNIX_OFFSET = 978307200.0

class BatSao(SpacecraftFrameModelMixin, SpacecraftStatesModelMixin, FitsFileContextManager):
    """Class for reading a GBM Position history file.
    """
    def get_spacecraft_frame(self) -> SpacecraftFrame:
        # q1 = self.ndim_column_as_array(1, 'QUATERNION', 0).byteswap().newbyteorder()
        # q2 =self.ndim_column_as_array(1, 'QUATERNION', 1).byteswap().newbyteorder()
        # q3 = self.ndim_column_as_array(1, 'QUATERNION', 2).byteswap().newbyteorder()
        # q4 = self.ndim_column_as_array(1, 'QUATERNION', 3).byteswap().newbyteorder()

        sc_frame = SpacecraftFrame(
            obsgeoloc=r.CartesianRepresentation(
                x = self.ndim_column_as_array(1, 'POSITION', 0).byteswap().newbyteorder(),
                y = self.ndim_column_as_array(1, 'POSITION', 1).byteswap().newbyteorder(),
                z = self.ndim_column_as_array(1, 'POSITION', 2).byteswap().newbyteorder(),
                unit=u.m
            ),
            obsgeovel=r.CartesianRepresentation(
                x=self.ndim_column_as_array(1, 'VELOCITY', 0).byteswap().newbyteorder() ,
                y=self.ndim_column_as_array(1, 'VELOCITY', 1).byteswap().newbyteorder(),
                z=self.ndim_column_as_array(1, 'VELOCITY', 2).byteswap().newbyteorder(),
                unit=u.m/u.s
            ),
            quaternion=Quaternion(self.column(1,'QUATERNION').byteswap().newbyteorder()),
            obstime=Time(self.column(1, 'TIME'), format='swift')
        )
        print(sc_frame
        )
        return sc_frame

    def get_spacecraft_states(self) -> TimeSeries:
        saa = self._in_saa(self.column(1, 'SAA'))
        series = TimeSeries(
            time=Time(self.column(1, 'TIME'), format='swift'),
            data={
                'sun': self._in_sun(self.column(1, 'SUNSHINE')),
                'saa': saa,
            }
        )
        return series

    def ndim_column_as_array(self, hdu_num: int, col_name: str, arr_num: int)-> np.array:
        """Return a list of columns from an HDU as an array.

        Args:
            hdu_num (int): The HDU number
            col_names (list of str): The names of the columns
            dtype (np.dtype, optional): The custom dtype of the output array

        Returns:
            (np.array)
        """
        items = self.column(hdu_num, col_name)
        new_array = []
        for item in items:
            new_array += [item[arr_num]]
        return np.array(new_array)

    @classmethod
    def open(cls, file_path, **kwargs):
        """Open a Swift BAT SAO FITS file.

        Args:
            file_path (str): The file path of the FITS file

        Returns:
            (:class:`BatSAO`)
        """
        obj = super().open(file_path, **kwargs)
        hdrs = [hdu.header for hdu in obj.hdulist]
        obj._headers = SaoHeaders.from_headers(hdrs)
        print (obj)
        return obj

    @staticmethod
    def _in_sun(flags: np.array) -> np.array:
        return (flags & 0x01) != 0

    @staticmethod
    def _in_saa(flags: np.array) -> np.array:
        return (flags & 0x02) != 0
