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
import astropy.units as u
from gdt.core.detector import Detectors
from astropy import wcs
import healpy as hp
import astropy.io.fits as fits
import numpy as np
from gdt.core.plot.sky import EquatorialPlot
from scipy.spatial.transform import Rotation
from copy import deepcopy
from matplotlib.pyplot import contour as Contour

__all__ = ['BatPartialCoding', 'BatDetector']

# unfortunately Sphinx has a major bug that prevents the autodoc of Enums,
# so we have to define all of this in the docstring...

data_path = '/Users/cfletch3/Documents/Research/GBM/GDT/gdt_devel/gdt-swift/src/gdt/missions/swift/bat/'
_file = data_path + 'pcode_default.img'
class BatPartialCoding():
    nside = 128
    def __init__(self):
        hdulist = fits.open(_file, memmap=False)
        w = wcs.WCS(hdulist[0].header)
        data = hdulist[0].data

        num_y, num_x = w.array_shape
        x = np.arange(num_x)
        y = np.arange(num_y)
        x, y = np.meshgrid(x, y)
        ra, dec = w.wcs_pix2world(x, y, 1)
        ra += 360.0

        npix = hp.nside2npix(self.nside)
        pix = hp.ang2pix(self.nside, ra, dec, lonlat=True)
        self._hpx = np.zeros(npix)
        self._hpx[pix] = data.reshape(pix.shape)

    def partial_coding_path(self, frac, numpts_ra=360, numpts_dec=180):
        """Return the bounding path for a given partial coding fraction

        Args:
            frac (float): The partial coding fraction (valid range 0-1)
            numpts_ra (int, optional): The number of grid points along the RA
                                       axis. Default is 360.
            numpts_dec (int, optional): The number of grid points along the Dec
                                        axis. Default is 180.

        Returns:
            [(np.array, np.array), ...]: A list of RA, Dec points, where each \
                item in the list is a continuous closed path.
        """
        # create the grid and integrated probability array
        grid_pix, phi, theta = self._mesh_grid(numpts_ra, numpts_dec)
        frac_arr = self._hpx[grid_pix]

        ra = self._phi_to_ra(phi)
        dec = self._theta_to_dec(theta)
        print(ra,dec)
        # use matplotlib contour to produce a path object
        contour = Contour(ra, dec, frac_arr, [frac])

        # get the contour path, which is made up of segments
        paths = contour.collections[0].get_paths()

        # extract all the vertices
        pts = [path.vertices for path in paths]

        # unfortunately matplotlib will plot this, so we need to remove
        for c in contour.collections:
            c.remove()

        return pts

    def rotate(self, quaternion):
        # use scipy to convert between quaternion and euler angle, which is
        # what healpy uses
        eulers = Rotation.from_quat(quaternion).as_euler('ZYX')

        # rotate partial coding map according to euler angle
        rotator = hp.Rotator(rot=np.rad2deg(eulers))
        rot_hpx = rotator.rotate_map_pixel(self._hpx)
        # rotate it again because the reference frame for the map is in
        # equatorial coordinates instead of spacecraft coordinates
        rotator = hp.Rotator(rot=[0.0, 0.0, 90.0])
        rot_hpx = rotator.rotate_map_pixel(rot_hpx)

        obj = deepcopy(self)
        obj._hpx = rot_hpx
        return obj

    def _mesh_grid(self, num_phi, num_theta):
        # create the mesh grid in phi and theta
        theta = np.linspace(np.pi, 0.0, num_theta)
        phi = np.linspace(0.0, 2 * np.pi, num_phi)
        phi_grid, theta_grid = np.meshgrid(phi, theta)
        grid_pix = hp.ang2pix(self.nside, theta_grid, phi_grid)
        return (grid_pix, phi, theta)

    @staticmethod
    def _phi_to_ra(phi):
        return np.rad2deg(phi)

    @staticmethod
    def _theta_to_dec(theta):
        return np.rad2deg(np.pi / 2.0 - theta)

class BatDetector(Detectors):
    """The Bat Detector name and orientation definitions.

    .. rubric:: Attributes Summary
    .. autosummary::

      azimuth
      elevation
      full_name
      number
      zenith

    .. rubric:: Methods Summary

    .. autosummary::

      bgo
      from_full_name
      from_num
      from_str
      is_bgo
      is_nai
      nai
      pointing
      skycoord

    .. rubric:: Attributes Documentation

    .. autoattribute:: azimuth
    .. autoattribute:: elevation
    .. autoattribute:: full_name
    .. autoattribute:: number
    .. autoattribute:: zenith

    .. rubric:: Methods Documentation

    .. autoattribute:: bgo
    .. automethod:: from_full_name
    .. automethod:: from_num
    .. automethod:: from_str
    .. automethod:: is_bgo
    .. automethod:: is_nai
    .. autoattribute:: nai
    .. automethod:: pointing
    .. automethod:: skycoord
    """
    bat = ('BAT', 0, 0.0 * u.deg, 0.0 * u.deg)


    @classmethod
    def bat_det(cls):
        """Get all detectors that are BAT

        Returns:
            (list of :class:`BAT Detectors`)
        """
        return [x for x in cls if x.is_bat()]


    def is_bat(self):
        """Check if detector is an Bat.

        Returns:
            (bool)
        """
        return self.name[0] == 'bat'
