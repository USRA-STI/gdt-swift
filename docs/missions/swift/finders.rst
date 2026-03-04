.. _swift-finders:
.. |SwiftObsFinder| replace:: :class:`~gdt.missions.swift.finders.SwiftObsFinder`
.. |SwiftAuxilFinder| replace:: :class:`~gdt.missions.swift.finders.SwiftAuxilFinder`
.. |SwiftTemporalFinder| replace:: :class:`~gdt.missions.swift.finders.SwiftTemporalFinder`
.. |SwiftAuxilTemporalFinder| replace:: :class:`~gdt.missions.swift.finders.SwiftAuxilTemporalFinder`
.. |get()| replace:: :meth:`~gdt.missions.swift.finders.SwiftObsFinder.get`

.. 
**************************************************************
Swift Data Finders (:mod:`gdt.missions.swift.finders`)
**************************************************************
Swift data are stored relative to an observation ID (ObsID), where the ObsID 
organizes observations belonging to the same target or object of interest. 
The data files associated with an ObsID may contain many data segments 
separated by long periods of null data when the spacecraft slews to look at 
another target or the Earth occults the target before Swift can get back on 
target.  Swift may even revisit the target again days or weeks later, and so
the archive is organized in a hybrid time-ObsID way, where one must know both 
the month of observation *and* the ObsID in order to find the data for a given 
observation.  

Finding Swift Observations with a Time and an ObsID
===================================================
If you know the ObsID and a time of interest, then finding the data you want is
easy.  This is generally performed by the |SwiftObsFinder| base class, which
is inherited by |SwiftAuxilFinder| to find files such as the orbit position and
pointing history during the observation.

This is used in the following way:
Let's say we want these files for ObsID 00098298003 on December 1, 2025:
    
    >>> from gdt.missions.swift.time import *
    >>> from gdt.missions.swift.finders import SwiftAuxilFinder
    >>> t0 = Time('2025-12-01 12:00:00')
    >>> obsid = '00098298003'
    >>> finder = SwiftAuxilFinder(t0, obsid)
    >>> print(finder)
    <SwiftAuxilFinder: 2025-12-01 12:00:00.000, 00098298003>
    
We can see what archive directory we are in with the following:

    >>> finder.cwd
    '/swift/data/obs/2025_12/00098298003/auxil'

And we can get a listing of files in the directory:
    
    >>> finder.files
    ['SWIFT_TLE_ARCHIVE.txt.25344.16528503.gz',
     'sw00098298003pat.fits.gz',
     'sw00098298003pjb.par.gz',
     'sw00098298003pob.cat.gz',
     'sw00098298003ppr.par.gz',
     'sw00098298003s.mkf.gz',
     'sw00098298003sao.fits.gz',
     'sw00098298003sat.fits.gz',
     'sw00098298003sen.hk.gz',
     'sw00098298003sti.fits.gz',
     'sw00098298003uat.fits.gz',
     'sw00098298003x.mkf.gz']

We can download the full file list or a subset of the list using the |get()|
method.

    >>> # download full file list
    >>> download_paths = finder.get('download_dir', finder.files)


Finding Swift Observations with Only a Time
===========================================
The problem with finding Swift data arises whenever one does not have the ObsID
on hand.  For example, perhaps you want to know the pointing history of Swift
over some time range.  In the previous example, you would need to know all of
the ObsIDs spanning that time range, which is not trivial.  This is the use
case for the |SwiftTemporalFinder| base class.  It allows you to search by a
time or time range and finds the files that contain data within that range.
This is done by first querying the 
`Swift Master Catalog <https://heasarc.gsfc.nasa.gov/w3browse/swift/swiftmastr.html>`_
with the `Start_Time` and `Stop_Time` parameters and returning the ObsIDs that
**potentially** (more on this in a bit) contain data during the time range that 
you are interested in.  Because the data from different ObsIDs are stored in 
different directories, |SwiftTemporalFinder| internally creates a 
|SwiftObsFinder| for each ObsID, but it seamlessly presents the contents to 
the user as if the data are all in a single directory for download.

The data that is found by |SwiftTemporalFinder| is the set of data that is 
bounded by all of the ObsIDs returned by the Swift Master Catalog for the time
range of interest.  That is to say that just because a file is found it does not
imply that the data you are looking for is in the file.  The very reason for 
this is based on the architectural decision to organize the archive by target 
observations instead of in the time domain (or instead of storing the data 
"as collected"). One file corresponding to one ObsID may be null at the time of
interest because Swift was observing a different target at that time, in which
case the data will be in one of the other files corresponding to a different 
ObsID. The only way to determine which file contains the data you need is to
read each file until you find the correct one. While this is not much of an 
issue for the auxiliary data (orbit and pointing history), it is a much larger 
problem for the science data and is out of scope for the data finders.

Let's see how this works with the auxiliary data.  We will use the 
|SwiftAuxilTemporalFinder| class for this, and we want the data within a 2-hour
window between 12:00 and 14:00 UTC on December 1, 2025:

    >>> from gdt.missions.swift.finders import SwiftAuxilTemporalFinder
    >>> t0 = Time('2025-12-01 12:00:00')
    >>> t1 = Time('2025-12-01 14:00:00')
    >>> finder = SwiftAuxilTemporalFinder(t0, tstop=t1)
    >>> print(finder)
    <SwiftAuxilTemporalFinder: 2025-12-01 12:00:00.000, 2025-12-01 14:00:00.000>

Now, we can see what directories contain the file(s) that we are interested in

    >>> finder.cwd
    ['/swift/data/obs/2025_11/00092103033/auxil',
     '/swift/data/obs/2025_12/00032613226/auxil',
     '/swift/data/obs/2025_12/00097905006/auxil',
     '/swift/data/obs/2025_12/00090560007/auxil']

As we can see, instead of a single path for the directory, we now have a total
of 4 paths where the files exist that cover the timespan that we are interested
in.  We can list all of the files if we want, or just simply get a file count:

    >>> finder.num_files
    48

A total of 48 files exist across the 4 directories covering our time of 
interest.  We can download all of them if we want, but maybe we are only 
interested in the orbit files.  There is a function that allows us to only
list and download those files:

    >>> # list the orbit files
    >>> finder.ls_orbit()
    ['sw00092103033sao.fits.gz',
     'sw00032613226sao.fits.gz',
     'sw00097905006sao.fits.gz',
     'sw00090560007sao.fits.gz']
    
    >>> # download the orbit files
    >>> orbit_filepaths = finder.get_orbit('download_dir')

Similarly, the spacecraft attitude (pointing) files can be listed and downloaded.
There are different types of attitude files, so we can choose which type to list
or download:

    >>> # list uncorrected attitude files
    >>> finder.ls_attitude(which='sat')
    ['sw00092103033sat.fits.gz',
     'sw00032613226sat.fits.gz',
     'sw00097905006sat.fits.gz',
     'sw00090560007sat.fits.gz']
    
    >>> # list best available attitude files
    >>> finder.ls_attitude(which='best')
    ['sw00092103033uat.fits.gz',
     'sw00032613226uat.fits.gz',
     'sw00097905006uat.fits.gz',
     'sw00090560007uat.fits.gz']


Table of Swift Auxiliary Data Products
======================================


.. list-table::
  :widths: 25 50
  :header-rows: 1

  * - File Name
    - Description
  * - sw[obs-id]sat.fits
    - uncorrected attitude information
  * - sw[obs-id]sao.fits
    - orbit information
  * - sw[obs-id]sen.fits
    - spacecraft engineering parameters
  * - sw[obs-id]s.mkf
    - filter file where the attitude and the instrument housekeeping (HK) paramaters are collected for use during screening
  * - sw[obs-id]sti.mkf
    - UTCF timing correction for the observation
  * - sw[obs-id]pob.cat
    - Catalog file listing all the files within the observation
  * - sw[obs-id]ppr.par
    - processing parameter file (ASCII)
  * - sw[obs-id]pjb.par
    - 'job' parameter file (ASCII)
  * - SWIFT_TLE_ARCHIVE.txt.
    - two-line element file used in the orbit derivation (ASCII)
  * - sw[obs-id]pat.fits
    - smoothed attitude on-ground
  * - sw[obs-id]uat.fits
    - attitude calibrated with UVOT observations (best)



Reference/API
=============

.. automodapi:: gdt.missions.swift.finders
   :inherited-members:
