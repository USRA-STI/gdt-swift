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
from copy import deepcopy
from pathlib import Path
from astropy import wcs
import astropy.io.fits as fits
import healpy as hp
from matplotlib.pyplot import contour as Contour
import numpy as np
from scipy.spatial.transform import Rotation

from gdt.core.healpix import HealPix
from gdt.core.plot.plot import SkyPolygon

#__all__ = ['BatPartialCoding']

class HealPixPartialCoding(HealPix):
    """Class supporting HEALPix operatings for coded-aperture partial coding.
    """
    @property
    def pcoding(self):
        """(np.array): The partial coding fraction HEALPix array"""
        return self._hpx
    
    def area(self, fraction):
        """Calculate the area, in square degrees, covered by a given partial 
        coding fraction.
        
        Args:
            fraction (float): The partial coding fraction (between 0 and 1).
        
        Returns:
            (float)
        """
        if fraction < 0.0 or fraction > 1.0:
            raise ValueError('fraction must be between 0 and 1')
        num_pix = (self.pcoding >= fraction).sum()
        return num_pix * self.pixel_area
    
    def partial_coding(self, az, zen):
        """Calculate the partial coding at a given point.  This
        function interpolates the map at the requested point rather than
        providing the vale at the nearest pixel center.

        Args:
            az (float): The Azimuth
            zen (float): The Zenith

        Returns:
            (float)
        """
        phi = self._ra_to_phi(az)
        theta = np.deg2rad(zen)
        pcoding = hp.get_interp_val(self.pcoding, theta, phi)
        return pcoding

    def partial_coding_path(self, fraction, numpts_az=360, numpts_zen=180):
        """Return the bounding path for a given partial coding fraction

        Args:
            fraction (float): The partial coding fraction (valid range 0-1)
            numpts_az (int, optional): The number of grid points along the 
                                       azimuthal axis. Default is 360.
            numpts_zen (int, optional): The number of grid points along the
                                        polar axis. Default is 180.

        Returns:
            [(np.array, np.array), ...]: A list of Az, Zen points, where each 
                item in the list is a continuous closed path.
        """
        if fraction < 0.0 or fraction > 1.0:
            raise ValueError('fraction must be between 0 and 1')
        
        # create the grid and integrated probability array
        grid_pix, phi, theta = self._mesh_grid(numpts_az, numpts_zen)
        frac_arr = self.pcoding[grid_pix]
        az = self._phi_to_ra(phi)
        zen = self._theta_to_dec(theta)

        # use matplotlib contour to produce a path object
        contour = Contour(az, zen, frac_arr, [fraction])

        # extract all the vertices
        pts = contour.allsegs[0]

        # unfortunately matplotlib will plot this, so we need to remove
        contour.remove()

        return pts

    def _assert_pcoding(self, pcoding):
        """Ensures partial coding array is between 0-1"""
        pcoding[(pcoding > 1.0)] = 1.0
        pcoding[(pcoding < 0.0)] = 0.0
        return pcoding
        
  
class BatPartialCoding(HealPixPartialCoding):
    """Represents the Swift BAT partial coding fraction in HEALPix.
    
    Parameters:
        nside (int, optional): The NSIDE resolution at which to create the 
                               partial coding map. Default is 128.
    """
    _path = Path(__file__).resolve().parent / 'data' / 'pcode_default.img'
    
    def __init__(self, nside=128):
        super().__init__()
        
        self._nside = nside
        
        with fits.open(self._path) as hdulist:
            # the file stores in celestial coordinates instead of spacecraft
            # this is a simple 90 deg rotation at read time into Az/Zen
            hdulist[0].header['CRVAL2'] = 90.0 - hdulist[0].header['CRVAL2']
            w = wcs.WCS(hdulist[0].header)
            data = hdulist[0].data
        
        # generate a grid of azimuth and zenith based on the WCS
        num_y, num_x = w.array_shape
        x = np.arange(num_x)
        y = np.arange(num_y)
        x, y = np.meshgrid(x, y)
        az, zen = w.wcs_pix2world(x, y, 1)
        az += 360.0
        
        # create and fill the HEALPix array
        npix = hp.nside2npix(self._nside)
        pix = hp.ang2pix(self._nside, ra, dec, lonlat=True)
        self._hpx = np.zeros(npix)
        self._hpx[pix] = self._assert_pcoding(data.reshape(pix.shape))

    def make_polygon(self, fraction, ax, **kwargs):
        
        paths = self.partial_coding_path(fraction)
        
        polys = []
        for path in paths:
            poly = SkyPolygon(path[:,0], path[:,1], ax, flipped=False, frame='spacecraft',
                              **kwargs)
            polys.append(poly)
        return polys

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
