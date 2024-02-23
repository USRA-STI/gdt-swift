.. _swift-time:

*****************************************************
Swift Mission Epoch  (:mod:`gdt.missions.swift.time`)
*****************************************************

The Swift Mission epoch, also called the Swift Mission Elapsed Time (MET) is
the number of seconds elapsed since January 1, 2001, 00:00:00 UTC, including
leap seconds.  We have defined a specialized epoch to work with Astropy ``Time``
objects so that Swift MET can be easily converted to/from other formats and time
scales.

To use this, we simply import and create an astropy Time object with a `'swift'`
format:

    >>> from gdt.missions.swift.time import Time
    >>> swift_met = Time(697422649, format='swift')
    >>> swift_met
    <Time object: scale='tt' format='swift' value=697422649.0>

Now, say we want to retrieve the GPS timestamp:

    >>> swift_met.gps
    1359765062.0

The Astropy ``Time`` object readily converts it for us. We can also do the
reverse conversion:

    >>> gps_time = Time(swift_met.gps, format='gps')
    >>> gps_time
    <Time object: scale='tai' format='gps' value=1359765062.0>

    >>> gps_time.swift
    697422649.0

And we should, of course, get back the Swift MET we started with.  This enables
you do do any time conversions already provided by Astropy, as well as time
conversions between other missions within the GDT.

In addition to time conversions, all time formatting available in Astropy is
also available here.  For example, we can format the Swift MET in ISO format:

    >>> swift_met.iso
    '2023-02-07 00:31:53.184'


Reference/API
=============

.. automodapi:: gdt.missions.swift.time
   :inherited-members:
