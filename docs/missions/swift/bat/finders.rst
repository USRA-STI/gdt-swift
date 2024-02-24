.. _bat-finders:
.. |BatAuxiliaryFtp| replace:: :class:`~gdt.missions.swift.bat.finders.BatAuxiliaryFtp`
.. |BatDataProductsFtp| replace:: :class:`~gdt.missions.swift.bat.finders.BatDataProductsFtp`
.. 
**************************************************************
Swift BAT Data Finders (:mod:`gdt.missions.swift.bat.finders`)
**************************************************************
A natural question may be: "Where do I find the data I need?" Well, you're in
luck, because this will show you how to find the data you seek. bat Data is
hosted publicly on the HEASARC FTP server
and the data are stored in a consistent directory structure. But instead of
having to navigate a winding maze of FTP directories, we provide a couple of
classes built to retrieve the data you want. These finders are currently setup to download data for Swift BAT GRBs and have been processed by the pipeline as well as the Auxiliary files that provide the spacecraft information.
An analysis thread on how to perform the GRB processing script is 'here<https://swift.gsfc.nasa.gov/analysis/threads/batgrbproductthread.html>', although this is done automatically by the Swift pipeline.

Finding Pipeline Processed BAT Data
===================================

Let's start with the pipeline processed GRB data. To download the data you will need to know the observtation ID which is an 11 digit sequence number that identifies the observation. GRB data that has been processed with the BAT pipeline will have an observation ID ended in '000'. You will need to know the observation ID number you're
interested in (01116441) and the year and month ('2022-07') of the GRB:

    >>> from gdt.missions.swift.bat.finders import TriggerFtp
    >>> finder = BatDataProductsFtp('01116441', '2022-07')
    <TriggerFtp: 190114873>
    >>> finder.num_files
    122

We don't really care about the directory structure, we just want the data. So
this quickly gets us to the directory we need. There are 14 files associated
with this GRB. Say we want to all the data available.

    >>> finder.ls_cspec()
    ['sw01116441000bev1s.lc.gz',
     'sw01116441000bev1s_lc.gif',
     'sw01116441000bev_skim.gif',
     'sw01116441000bevas_dt.img.gz',
     'sw01116441000bevas_sk.img.gz',
     'sw01116441000bevbu.gti.gz',
     'sw01116441000bevms.lc.gz',
     'sw01116441000bevpb_dt.img.gz',
     'sw01116441000bevpb_sk.img.gz',
     'sw01116441000bevps.pha.gz',
     'sw01116441000bevps.rsp.gz',
     'sw01116441000bevps_dt.img.gz',
     'sw01116441000bevps_sk.img.gz',
     'sw01116441000bevsl.pha.gz']

Great! There's a full complement of BAT Pipeline data. How about we download this data to a specified directory?

    >>> finder.det('downlaod-dir')
    sw01116441000bev1s.lc.gz ━━━━━━━━━━━ 100.0% • 88.7/88.7   • 271.6 kB/s • 0:00:00
    sw01116441000bev1s_lc.gif ━━━━━━━━━━ 100.0% • 21.4/21.4   • 137.3 MB/s • 0:00:00
    sw01116441000bev_skim.gif ━━━━━━━━━━ 100.0% • 100.6/100.6 • 791.6 kB/s • 0:00:00
    sw01116441000bevas_dt.img.gz ━━━━━━━━━ 100.0% • 193.0/193… • 438.6 kB/s • 0:00:00
    sw01116441000bevas_sk.img.gz ━━━━━━━━━━ 100.0% • 11.9/11.9  • 6.7 MB/s • 0:00:00
    sw01116441000bevbu.gti.gz ━━━━━━━━━━━━━━━━━━━━ 100.0% • 4.1/4.1 kB • ? • 0:00:00
    sw01116441000bevms.lc.gz ━━━━━━━━━━━━━━ 100.0% • 1.3/1.3 MB • 1.8 MB/s • 0:00:00
    sw01116441000bevpb_dt.img.gz ━━━━━━━━━ 100.0% • 167.2/167… • 586.2  kB/s    • 0:00:00
    sw01116441000bevpb_sk.img.gz ━━━━━━━━━━ 100.0% • 11.3/11.3  • 3.7 MB/s • 0:00:00
    sw01116441000bevps.pha.gz ━━━━━━━━━━━ 100.0% • 9.8/9.8 kB • 101.2 MB/s • 0:00:00
    sw01116441000bevps.rsp.gz ━━━━━━━━━━ 100.0% • 46.5/46.5   • 621.9 kB/s • 0:00:00
    sw01116441000bevps_dt.img.gz ━━━━━━━━━ 100.0% • 117.2/117… • 337.4 kB/s    • 0:00:00
    sw01116441000bevps_sk.img.gz ━━━━━━━━━━ 100.0% • 10.8/10.8  • 5.6 MB/s • 0:00:00
    sw01116441000bevsl.pha.gz ━━━━━━━━━━━━ 100.0% • 9.8/9.8 kB • 97.9 MB/s • 0:00:00



Finding Auxiliary BAT Data
==========================
Now we want the auxiliary data which describes the spacecraft position/orientation files. A breakdown of these data products are in :ref:list-table. To find the data you
need, instead of a trigger number, you need to create a |BatAuxiliaryFtp|
object by specifying a time using Astropy Time:

    >>> from gdt.missions.swift.bat.finders import BatAuxiliaryFtp
    >>> aux_finder = BatAuxiliaryFtp('01116441', '2022-07')
    >>> aux_finder
    <ContinuousFtp: 587683338.0>
    >>> aux_finder.num_files
    12

That's a whole lotta files in this directory. Most of them are TTE; remember
that each hour has a TTE file (since the end of 2012) for each detector. Let's
just list the CTIME that's available:

    >>> aux_finder.ls_all()
    ['SWIFT_TLE_ARCHIVE.txt.22202.86649910.gz',
     'sw01116441000pat.fits.gz',
     'sw01116441000pjb.par.gz',
     'sw01116441000pob.cat.gz',
     'sw01116441000ppr.par.gz',
     'sw01116441000s.mkf.gz',
     'sw01116441000sao.fits.gz',
     'sw01116441000sat.fits.gz',
     'sw01116441000sen.hk.gz',
     'sw01116441000sti.fits.gz',
     'sw01116441000uat.fits.gz',
     'sw01116441000x.mkf.gz']

Now let's list the available TTE for this time. This will only list the TTE
files in the directory that cover the relevant time:

    >>> aux_finder.get_all()
    SWIFT_TLE_ARCHIVE.txt.22202.86649910.gz ━━━━━━━━━━━ 100.0% • 174.6/174.6 • 832.1 kB/s • 0:00:00
    sw01116441000pat.fits.gz ━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 489.7/489.7 kB • 1.5 MB/s • 0:00:00
    sw01116441000pjb.par.gz ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 2.5/2.5 kB • ? • 0:00:00
    sw01116441000pob.cat.gz ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 7.3/7.3 kB • ? • 0:00:00
    sw01116441000ppr.par.gz ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 1.7/1.7 kB • ? • 0:00:00
    sw01116441000s.mkf.gz ━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 177.2/177.2 kB • 417.9 kB/s • 0:00:00
    sw01116441000sao.fits.gz ━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 608.2/608.2 kB • 982.9 kB/s • 0:00:00
    sw01116441000sat.fits.gz ━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 495.8/495.8 kB • 1.2 MB/s • 0:00:00
    sw01116441000sen.hk.gz ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 1.9/1.9 MB • 2.2 MB/s • 0:00:00
    sw01116441000sti.fits.gz ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 6.2/6.2 kB • ? • 0:00:00
    sw01116441000uat.fits.gz ━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 352.8/352.8 kB • 607.4 kB/s • 0:00:00
    sw01116441000x.mkf.gz ━━━━━━━━━━━━━━━━━━━━━━━━━━ 100.0% • 177.2/177.2 kB • 811.4 kB/s • 0:00:00


See :external:ref:`The FtpFinder Class<core-heasarc-finder>` for more details
on using data finders.

Data Products Descriptions:
===========================
The following descriptions were found in links '/https://swift.gsfc.nasa.gov/analysis/bat_swguide_v6_3.pdf' and 'https://swift.gsfc.nasa.gov/archive/archiveguide1/node5.html'. Not all of these data files may be in the directory you are working with.

.. list-table:: Pipline Data Products
   :widths: 25 50
   :header-rows: 1

   * - File Name
     - Description
   * - sw[obs-id]bev1s.lcv
     - BAT Light curve with 1-second bins and 4 energy bands(includes data taken during slew)
   * - sw[obs-id]bevms.lc
     - BAT Light curve with 64-msec bins and 4 energy bands
   * - sw[obs-id]bevbu.gti
     - Burst time intervals(T50, T90, T100, Tpeak, and background intervals)
   * - sw[obs-id]bevpb_dt.img
     - BAT Detector image for pre-burst interval
   * - sw[obs-id]bevpb_sk.img
     - BAT Sky image for pre-burst interval
   * - sw[obs-id]bevps_dt.img
     - BAT Detector image for pre-slew burst interval
   * - sw[obs-id]bevps_sk.img
     - BAT Skyimage for pre-slew burst interval
   * - sw[obs-id]bevps.pha
     - BAT Spectrum for pre-slew burst interval
   * - sw[obs-id]bevps.rsp
     - BAT Response matrix for pre-slew spectrum
   * - sw[obs-id]bevsl.pha
     - BAT Spectrum for slew burst interval
   * - sw[obs-id]bevas_dt.img
     - BAT Detector image for post-slew burst interval
   * - sw[obs-id]bevas_sk.img
     - BAT Sky image for post-slew burst interval
   * - sw[obs-id]bevas.pha
     - BAT Spectrum for post-slew burst interval
   * - sw[obs-id]bevas.rsp
     - BAT Response matrix for post-slew spectrum


.. list-table:: Auxiliary Data Products
  :widths: 25 50
  :header-rows: 1

  * - File Name
    - Description
  * - sw[obs-id]sat.fits
    - attitude information.
  * - sw[obs-id]sao.fits
    - orbit information.
  * - sw[obs-id]sen.fits
    - spacecraft engineering parameters.
  * - sw[obs-id]s.mkf
    - filter file where the attitude and the instrument housekeeping (HK) paramaters are collected for use during screening.
  * - sw[obs-id]sti.mkf
    - UTCF timing correction for the observation.
  * - sw[obs-id]pob.cat
    - Catalog file listing all the files within the observation.
  * - sw[obs-id]ppr.par
    - processing parameter file (ASCII).
  * - sw[obs-id]pjb.par
    - 'job' parameter file (ASCII).
  * - SWIFT_TLE_ARCHIVE.txt.
    - Two line element file used in the orbit derivation (ASCII).
  * - sw[obs-id]pat.fits
    - Processed attitude[#]_
  * - sw[obs-id]uat.fits
    - UVOT attitude[#]_

[#] Files were added to the auxil directories in 2007






Reference/API
=============

.. automodapi:: gdt.missions.swift.bat.finders
   :inherited-members:
