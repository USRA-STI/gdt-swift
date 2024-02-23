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
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

from gdt.core.plot.plot import EarthPoints, PlotElement, GdtCmap
from gdt.core.plot.earthplot import EarthPlot
from gdt.core.plot.sky import SkyPlot, SkyPolygon, SkyLine
from gdt.missions.swift.bat.poshist import BatSao
from gdt.missions.swift.bat.detectors import BatPartialCoding

__all__ = ['SwiftEarthPlot', 'SwiftIcon',  'BatFovPlot']

class SwftIcon(EarthPoints):
    """Plot a Bat icon on the Earth.

    Parameters:
        lat (np.array): The latitude value
        lon (np.array): The longitude value
        proj (GeoAxesSubplot): The Cartopy projection
        alpha (float, optional): The alpha opacity
        **kwargs: Other plotting options
    """
    def __init__(self, lat, lon, proj, alpha=1.0, **kwargs):
        self._norm_width = 31.4 * 2.0
        self._norm_height = 7.0 * 2.0
        super().__init__(lat, lon, proj, color=None, alpha=alpha, **kwargs)

    @property
    def lat(self):
        """(np.array): Normalized plot coordinates for the LAT"""
        return self._normalize(self._bat())

    @property
    def gbm_side(self):
        """(np.array): Normalized plot coordinates for the GBM side panel"""
        return self._normalize(self._gbm_side())

    @property
    def left_panel(self):
        """(np.array): Normalized plot coordinates for left panel + solar array"""
        return self._normalize(self._left_panel())

    @property
    def right_panel(self):
        """(np.array): Normalized plot coordinates for right panel + solar array"""
        return self._normalize(self._right_panel())

    @property
    def antenna(self):
        """(np.array): Normalized plot coordinates for antenna"""
        return self._normalize(self._antenna())

    def _create(self, lat, lon, proj):

        lon = np.asarray(lon)
        lat = np.asarray(lat)

        lon[(lon > 180.0)] -= 360.0
        x, y = (lon, lat)
        z = 10
        factor = 50.
        fermilat = self.lat * factor
        fermilat[:, 0] += x
        fermilat[:, 1] += y
        path1 = Path(fermilat, closed=True)
        patch1 = patches.PathPatch(path1, facecolor='#DCDCDC', zorder=z)
        proj.add_patch(patch1)

        gbm = self.gbm_side * factor
        gbm[:, 0] += x
        gbm[:, 1] += y
        path2 = Path(gbm, closed=True)
        patch2 = patches.PathPatch(path2, facecolor='#FFD700', zorder=z)
        proj.add_patch(patch2)

        panel = self.left_panel * factor
        panel[:, 0] += x
        panel[:, 1] += y
        path3 = Path(panel, closed=True)
        patch3 = patches.PathPatch(path3, facecolor='#45597C', zorder=z)
        proj.add_patch(patch3)

        panel = self.right_panel * factor
        panel[:, 0] += x
        panel[:, 1] += y
        path4 = Path(panel, closed=True)
        patch4 = patches.PathPatch(path4, facecolor='#45597C', zorder=z)
        proj.add_patch(patch4)

        antenna = self.antenna * factor
        antenna[:, 0] += x
        antenna[:, 1] += y
        path5 = Path(antenna, closed=True)
        patch5 = patches.PathPatch(path5, facecolor='#546165', zorder=z)
        proj.add_patch(patch5)

        return [patch1, patch2, patch3, patch4, patch5]

    def _normalize(self, pts):
        return (pts / self._norm_width)

    def _lat(self):
        pts = [[-2.5, 3.5], [-2.5, 1.2], [2.5, 1.2], [2.5, 3.5], [-2.5, 3.5]]
        pts = np.array(pts)
        return pts

    def _gbm_side(self):
        pts = [[-2.5, 1.2], [-2.5, -2.1], [2.5, -2.1], [2.5, 1.2], [-2.5, 1.2]]
        pts = np.array(pts)
        return pts

    def _left_panel(self):
        pts = [[-2.5, -1.0], [-4.5, -2.5], [-15.7, -2.5], [-15.7, 0.5],
               [-4.5, 0.5], [-2.5, -1.0]]
        pts = np.array(pts)
        return pts

    def _right_panel(self):
        pts = [[2.5, -1.0], [4.5, -2.5], [15.7, -2.5], [15.7, 0.5],
               [4.5, 0.5], [2.5, -1.0]]
        pts = np.array(pts)
        return pts

    def _antenna(self):
        pts = [[0.5, -2.1], [0.5, -3.5], [1.5, -3.5], [1.5, -2.1], [0.5, -2.1]]
        pts = np.array(pts)
        return pts


class SwiftEarthPlot(EarthPlot):
    """Class for plotting Swifts orbit

    Note:
        This class requires installation of Cartopy.

    Parameters:
        saa (:class:`~gdt.core.geomagnetic.SouthAtlanticAnomaly`, optional):
            If set, displays the region.

        **kwargs: Options to pass to :class:`~gdt.plot.plot.GdtPlot`
    """
    def __init__(self, saa=None, **kwargs):
        lat_range = (-30.00, 30.00)
        lon_range = (-180.0, 180.0)
        super().__init__(lat_range=lat_range, lon_range=lon_range, saa=saa,
                         **kwargs)

    def add_spacecraft_frame(self, *args, **kwargs):
        super().add_spacecraft_frame(*args, icon=SwiftIcon, **kwargs)

    def standard_title(self):
        """Add a standard plot title containing orbital position
        """
        if self.spacecraft is not None:
            coord = self.spacecraft.coordinates
            title = 'Latitude, East Longitude: ({0}, {1})\n'.format(*coord)
            lat = float(coord[0][:-1]) * (-1 if "S" in coord[0] else 1)
            lon = float(coord[1][:-1]) * (-1 if "W" in coord[1] else 1)
            self._m.set_title(title)


class BatFovPlot(SkyPlot):

    def add_bat_fov(self, frame):
        bat = BatPartialCoding()
        bat_rot = bat.rotate(frame.quaternion)
        fracs = [0.1, 0.5, 0.9]


        self.polys = []
        for frac in fracs:
            paths = bat_rot.partial_coding_path(frac)
            for path in paths:
                poly = SkyPolygon(path[:,0], path[:,1], self.ax, color = None, face_color='gray', edge_color='gray', flipped=True)
                poly.face_alpha=0.3
                self.polys.append(poly)



    def add_localization(self, frame):
        ra_dec = frame.get_src_position()
        print(ra_dec)
        self.points= []
        self.points.append(SkyLine(ra_dec[0], ra_dec[1], self.ax, flipped=True, color='g',
                         linestyle='none', marker="*", markersize=10, markeredgecolor='g',
                         markeredgewidth=.4))

    def add_pointing(self, frame):
        ra_dec = frame.get_bat_pointing()
        print(ra_dec)
        if self.points is None:
            self.points= []
        pointing = SkyLine(ra_dec[0], ra_dec[1], self.ax, flipped=True, color='r',
                         linestyle='none', marker="o", markersize=10, markeredgecolor='r',
                         markeredgewidth=.4)
        self.points.append(pointing)
