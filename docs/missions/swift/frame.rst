.. _swift-frame:
.. |SwiftFrame| replace:: :class:`~gdt.missions.swift.frame.SwiftFrame`
.. |GbmPosHist| replace:: :class:`~gdt.missions.swift.bat.poshist.BatSao`
.. |Quaternion| replace:: :class:`~gdt.core.coords.Quaternion`

********************************************************
Swift Spacecraft Frame (:mod:`gdt.missions.swift.frame`)
********************************************************

The Swift spacecraft frame, |SwiftFrame|, is the frame that is aligned
with the Swift spacecraft coordinate frame, and is represented by a
quaternion that defines the rotation from spacecraft coordinates to the ICRS
coordinate frame.  This frame takes advantage of the Astropy coordinate frame
design, so we can use the SwiftFrame to convert Astropy SkyCoord objects
between the SwiftFrame and any celestial frame.

While the SwiftFrame is typically initialized when reading from a mission
position history file (e.g. |GbmPosHist|) instead of manually by a user, we
can manually define the frame with a |Quaternion|:

    >>> from gdt.core.coords import Quaternion
    >>> from gdt.missions.swift.frame import *
    >>> quat = Quaternion([-0.218,  0.009,  0.652, -0.726], scalar_first=False)
    >>> swift_frame = SwiftFrame(quaternion=quat)
    >>> swift_frame
    <SwiftFrame: 1 frames;
     obstime=[J2000.000]
     obsgeoloc=[(0., 0., 0.) m]
     obsgeovel=[(0., 0., 0.) m / s]
     quaternion=[(x, y, z, w) [-0.218,  0.009,  0.652, -0.726]]>

Notice that we can also define the frame with an ``obstime``, which is useful
for transforming between the SwiftFrame and a non-inertial time-dependent frame;
an ``obsgeoloc``, which can define the spacecraft location in orbit; and
``obsgeovel``, which defines the spacecraft orbital velocity.

Now let us define a SkyCoord in RA and Dec:

    >>> from astropy.coordinates import SkyCoord
    >>> coord = SkyCoord(100.0, -30.0, unit='deg')

And we can simply rotate this into the Swift frame with the following:

    >>> swift_coord = coord.transform_to(swift_frame)
    >>> (swift_coord.az, swift_coord.el)
    (<Longitude [200.39733555] deg>, <Latitude [-41.88750942] deg>)

We can also transform from the Swift frame to other frames.  For example, we
define a coordinate in the Swift frame this way:

    >>> swift_coord = SkyCoord(50.0, 25.0, frame=swift_frame, unit='deg')

Now we can tranform to ICRS coordinates:

    >>> swift_coord.icrs
    <SkyCoord (ICRS): (ra, dec) in deg
        [(313.69000519, 26.89158349)]>

or Galactic coordinates:

    >>> swift_coord.galactic
    <SkyCoord (Galactic): (l, b) in deg
        [(71.5141302, -11.56931006)]>

or any other coordinate frames provided by Astropy.



Reference/API
=============

.. automodapi:: gdt.missions.swift.frame
   :inherited-members:
