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
from astropy.coordinates import FunctionTransform, ICRS, frame_transform_graph
from gdt.core.coords import *
from gdt.core.coords.spacecraft.frame import spacecraft_to_icrs, icrs_to_spacecraft

__all__ = ['SwiftFrame', 'swift_to_icrs', 'icrs_to_swift']

class SwiftFrame(SpacecraftFrame):
    """
    The Swift spacecraft frame in azimuth and elevation.  The frame is defined
    as a quaternion that represents a rotation from the Swift frame to the ICRS
    frame. This class is a wholesale inheritance of SpacecraftFrame

    Example use:

        >>> from gdt.core.coords import Quaternion
        >>> quat = Quaternion([-0.218,  0.009,  0.652, -0.726], scalar_first=False)
        >>> swift_frame = SwiftFrame(quaternion=quat)
        >>> coord = SkyCoord(100.0, -30.0, unit='deg')
        >>> az_el = SkyCoord.transform_to(swift_frame)
    """
    pass

@frame_transform_graph.transform(FunctionTransform, SwiftFrame, ICRS)
def swift_to_icrs(swift_frame, icrs_frame):
    """Convert from the Swift frame to the ICRS frame.

    Args:
        swift_frame (:class:`SwiftFrame`): The Swift frame
        icrs_frame (:class:`astropy.coordinates.ICRS`)

    Returns:
        (:class:`astropy.coordinates.ICRS`)
    """
    return spacecraft_to_icrs(swift_frame, icrs_frame)

@frame_transform_graph.transform(FunctionTransform, ICRS, SwiftFrame)
def icrs_to_swift(icrs_frame, swift_frame):
    """Convert from the ICRS frame to the Swift frame.

    Args:
        icrs_frame (:class:`astropy.coordinates.ICRS`)
        swift_frame (:class:`SwiftFrame`): The Swift frame

    Returns:
        (:class:`SwiftFrame`)
    """
    return icrs_to_spacecraft(icrs_frame, swift_frame)
