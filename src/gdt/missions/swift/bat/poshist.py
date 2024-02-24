# CONTAINS TECHNICAL DATA/COMPUTER SOFTWARE DELIVERED TO THE U.S. GOVERNMENT
# WITH UNLIMITED RIGHTS
#
# Grant No.: 80NSSC21K0651
# Grantee Name: Universities Space Research Association
# Grantee Address: 425 3rd Street SW, Suite 950, Washington DC 20024
#
# Copyright 2024 by Universities Space Research Association (USRA). All rights
# reserved.
#
# Developed by: Corinne Fletcher
#               Universities Space Research Association
#               Science and Technology Institute
#               https://sti.usra.edu
#
# This work is a derivative of the Gamma-ray Data Tools (GDT), including the
# Core and Fermi packages, originally developed by the following:
#
#     William Cleveland and Adam Goldstein
#     Universities Space Research Association
#     Science and Technology Institute
#     https://sti.usra.edu
#
#     Daniel Kocevski
#     National Aeronautics and Space Administration (NASA)
#     Marshall Space Flight Center
#     Astrophysics Branch (ST-12)
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
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
from .detectors import BatDetector, BatPartialCoding


__all__ = ['BatSao']

SWIFT_TO_UNIX_OFFSET = 978307200.0

class BatSao(SpacecraftFrameModelMixin, SpacecraftStatesModelMixin, FitsFileContextManager):
    """Class for reading a GBM Position history file.
    """
    def get_spacecraft_frame(self) -> SpacecraftFrame:

        sc_frame = SpacecraftFrame(
            obsgeoloc=r.CartesianRepresentation(
                x = self.ndim_column_as_array(1, 'POSITION', 0).byteswap().newbyteorder(),
                y = self.ndim_column_as_array(1, 'POSITION', 1).byteswap().newbyteorder(),
                z = self.ndim_column_as_array(1, 'POSITION', 2).byteswap().newbyteorder(),
                unit=u.km
            ),
            obsgeovel=r.CartesianRepresentation(
                x=self.ndim_column_as_array(1, 'VELOCITY', 0).byteswap().newbyteorder() ,
                y=self.ndim_column_as_array(1, 'VELOCITY', 1).byteswap().newbyteorder(),
                z=self.ndim_column_as_array(1, 'VELOCITY', 2).byteswap().newbyteorder(),
                unit=u.km/u.s
            ),
            quaternion=Quaternion(self.column(1,'QUATERNION').byteswap().newbyteorder()),
            obstime=Time(self.column(1, 'TIME'), format='swift'),
            detectors = BatDetector
        )


        return sc_frame

    def get_spacecraft_states(self) -> TimeSeries:
        series = TimeSeries(
            time=Time(self.column(1, 'TIME'), format='swift'),
            data={
                'sun': self.column(1, 'SUNSHINE'),
                'saa': self.column(1, 'SAA'),
            }
        )
        return series

    def get_bat_pointing(self):
        bat_ra = self.headers['PRIMARY']['RA_PNT']
        bat_dec = self.headers['PRIMARY']['DEC_PNT']
        return bat_ra, bat_dec

    def get_src_position(self):
        obj_ra = self.headers['PRIMARY']['RA_OBJ']
        obj_dec = self.headers['PRIMARY']['DEC_OBJ']
        return obj_ra, obj_dec

    def get_tstart(self):
        return self.headers['PRIMARY']['TSTART']

    def get_tstop(self):
        return self.headers['PRIMARY']['TSTOP']

    def time_range(self):
        return(self.get_tstart(), self.get_tstop())

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

        return obj
