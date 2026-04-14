.. _bat-poshist:
.. |SwiftSao| replace:: :class:`~gdt.missions.swift.poshist.SwiftSao`
.. |Gti| replace:: :class:`~gdt.core.data\_primitives.Gti`
.. |SpacecraftFrame| replace:: :class:`~gdt.core.coords.SpacecraftFrame`

********************************************************************************
Swift Position/Attitude History Data (:mod:`gdt.missions.swift.poshist`)
********************************************************************************
Probably the most critical auxiliary file Swift produces is the Spacecraft 
Attitude/Orbit (SAO) history file. The SAO contains the spacecraft
location in orbit and pointing information, sampled on a 1 second timescale.
You may want to know if a source is visible at a particular time
(i.e. not behind the Earth). You may want to know if there are specific 
contributions to the background during a time interval, such as sun visibility 
or high geomagnetic latitude in orbit. You may want to rotate something from 
the equatorial frame to the Swift inertial frame, or vice versa. Or you may want 
to make a pretty gif of the detector pointings over time.

To read a SAO file, we open it with the |SwiftSao| class:

    >>> from gdt.core import data_path
    >>> from gdt.missions.swift.poshist import SwiftSao
    >>> filepath = data_path / 'swift-bat' / 'sw00974827000sao.fits.gz'
    >>> sao = SwiftSao.open(filepath)
    >>> sao
    <SwiftSao(filename="sw00974827000sao.fits") at 0x7fd63d9ebd90>

The SwiftSao object contains the spacecraft **frame**, which is the spacecraft
position and orientation as a function of time, and the spacecraft **states**,
which are the series of state flags as a function of time.

To see what state flags are available, we can retrieve the spacecraft states
in the following way:

    >>> states = sao.get_spacecraft_states()
    >>> states
    <TimeSeries length=2162>
         time       sun   saa 
         Time      int16 int16
    -------------- ----- -----
    612353536.6006     0     0
    612353537.6006     0     0
    612353538.6006     0     0
    612353539.6006     0     0
    612353540.6006     0     0
    612353541.6006     0     0
    612353542.6006     0     0
    612353543.6006     0     0
    612353544.6006     0     0
               ...   ...   ...
    612355688.6006     1     0
    612355689.6006     1     0
    612355690.6006     1     0
    612355691.6006     1     0
    612355692.6006     1     0
    612355693.6006     1     0
    612355694.6006     1     0
    612355695.6006     1     0
    612355696.6006     1     0
    612355697.6006     1     0


The state flags are stored in an Astropy TimeSeries object, and for each
sampled time, there is a flag denoting if the sun is visible, if the spacecraft
is in SAA, and if the data are in a good time interval (which in this case is
just the opposite of the SAA flag).

We can, for example create a Good Time Intervals |Gti| object from the ``time``
and ``saa`` columns:

    >>> from gdt.core.data_primitives import Gti
    >>> gti = Gti.from_boolean_mask(states['time'].value, ~states['saa'].value)
    >>> gti
    <Gti: 1 intervals; range (612353536.6006, 612355697.6006)>

Regarding the spacecraft frame, we can retrieve it as a |SpacecraftFrame|
object:

    >>> frame = sao.get_spacecraft_frame()
    <SpacecraftFrame: 2162 frames;
    obstime=[612353536.6006, ...]
    obsgeoloc=[(-6165602., -2728582.2, 1604040.5) m, ...]
    obsgeovel=[(3400.097, -6478.7993, 2006.0916) m / s, ...]
    quaternion=[(x, y, z, w) [-0.35197902, -0.34436679, -0.75078022,  0.44028553], ...]>

You will notice that this frame has a location in Earth Inertial Coordinates
(``obsgeoloc``), the velocity of the spacecraft with reference to the Earth
Inertial Coordinate frame (``obsgeovel``), and the spacecraft orientation
quaternion, each for a given time stamp (``obstime``).

Let's say we are interested in data around a specific time, for example
MET=612355691.6006. We can generate an interpolated frame at the requested time, as
long as it exists within the boundaries of the file.

    >>> from gdt.missions.swift.time import *
    >>> time = Time(612355691.6006, format='swift')
    >>> one_frame = frame.at(time)
    >>> one_frame
    <SpacecraftFrame: 1 frames;
     obstime=[612355691.6006]
     obsgeoloc=[(6557780., -2207894.75, 134512.375) m]
     obsgeovel=[(2323.70922852, 6723.68066406, -2668.9206543) m / s]
     quaternion=[(x, y, z, w) [-0.2434614 ,  0.39559507, -0.55300576,  0.69167602]]>

We can retrieve where Swift was in orbit at that time:

    >>> one_frame.earth_location.lat, one_frame.earth_location.lon
    (<Latitude 1.22700959 deg>, <Longitude -66.81447614 deg>)
    >>> one_frame.earth_location.height
    <Quantity 542665.41017423 m>

We might be interested to know where the Earth is (and its apparent radius)
relative to Swift:

    >>> one_frame.geocenter.ra, one_frame.geocenter.dec
    (<Longitude 161.39248212 deg>, <Latitude -1.11366964 deg>)

    >>> one_frame.earth_angular_radius
    <Quantity 67.15947244 deg>

We could also be interested in a particular known source, and it would be
helpful to know if it is even visible to Swift at the time of interest:

    >>> from astropy.coordinates import SkyCoord
    >>> coord = SkyCoord(324.3, -20.8, frame='icrs', unit='deg')
    >>> one_frame.location_visible(coord)
    True

Well, that's good to know.

Sometimes it's useful to transform a source location of interest in equatorial
coordinates to the Swift inertial frame. You can do that by the following:

    >>> coord_sc_frame = coord.transform_to(one_frame)
    >>> coord_sc_frame.az, coord_sc_frame.el
    (<Longitude [39.65707981] deg>, <Latitude [28.22627833] deg>)

Note that the frame transformation is in azimuth and **elevation**.  It's
important to note that the Swift inertial frame is defined by azimuth
(0-360 deg) and elevation (-90-90 deg) or zenith (0-180 deg).

You can also go from Swift (azimuth, elevation) coordinates to equatorial
coordinates:

    >>> sc_coord = SkyCoord(0.0, 90.0, frame=one_frame, unit='deg')
    >>> sc_coord.icrs
    <SkyCoord (ICRS): (ra, dec) in deg
        [(352.96654199, 34.64305751)]>

Note that any and all of these operations can be performed on an array of
frames, even on the entire series of frames contained within the SAO file.
For more details on working with the |SpacecraftFrame|,
see :external:ref:`Spacecraft Attitude, Position, and Coordinates<core-coords>`.


Reference/API
=============

.. automodapi:: gdt.missions.swift.poshist
   :inherited-members:
