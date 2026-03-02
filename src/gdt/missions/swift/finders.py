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
import astropy.io.fits as fits
import numpy as np
import os
import ssl
from urllib.error import HTTPError
from urllib.request import urlopen
from urllib.parse import quote

from gdt.core import cache_path
from gdt.core.data_primitives import TimeRange, Intervals
from gdt.core.heasarc import BaseFinder
from .time import *


__all__ = ['SwiftAuxilFinder', 'SwiftObsFinder', 'SwiftAuxilTemporalFinder', 
           'SwiftTemporalFinder']


cache_path = os.path.join(cache_path, 'swift')


class SwiftObsFinder(BaseFinder):
    """A class that interfaces with the HEASARC FTP directories.
    An instance of this class will represent the available files associated
    with a single event.

    An instance can be created with an astropy Time object and an observation
    ID to query and download files. An instance can also be changed from one
    observation to another without having to create a new instance.

    Parameters:
        date (astropy.Time, optional): A time for the observation
        obsid (str, optional): A valid observation ID number
    """
    _root = '/swift/data/obs/'

    def _construct_path(self, date, obsid):
        """Constructs the FTP path for a observation

        Args:
            date (astropy.Time): The date/time
            obsid (str): The observation ID

        Returns:
            str: The path of the FTP directory for the observation
        """
        path = os.path.join(self._root, date.utc.strftime('%Y_%m'), obsid)
        return path


class SwiftAuxilFinder(SwiftObsFinder):
   
    def _construct_path(self, date, obsid):
        """Constructs the FTP path for a observation

        Args:
            date (astropy.Time): The date/time
            obsid (str): The observation ID

        Returns:
            str: The path of the FTP directory for the observation
        """
        path = os.path.join(self._root, date.utc.strftime('%Y_%m'), obsid, 
                            'auxil')
        return path


class SwiftTemporalFinder:
    """Find Swift data that covers a given time or time range.
    
    Swift data are not stored as continuous and contiguous time series, 
    therefore finding Swift data corresponding to a time or time range is 
    not a trivial exercise.  The data files are divided into observation IDs on 
    given dates, and the files with a given observation ID and date can in fact 
    contain data beyond that date. This class queries the Swift Master catalog
    to find all observation IDs that are contained within a specified time 
    range.  The files for each observation ID are stored in different directories,
    so this class interfaces with a :class:`SwiftObsFinder` class (or derived)
    to perform all finder operations over multiple directories.
    
    Note:
      Even though an observation ID spans a time range that contains a time of
      interest, this does not mean that a data file corresponding to that ID
      will contain data at that time.  For example, a query at a particular time
      may return 10 different observation IDs (and thus 10 different 
      directories), however, only one observation ID will actually contain data
      at the given time. Unfortunately there is no way to determine which file
      contains the desired data without opening each file and checking for data
      availability at that time, an activity that is beyond the scope of this
      class.
    
    
    This is a base clase. Inherited classes must set the class variable 
    `_base_obs_finder` to the respective finder.
    
    
    Parameters:
        tstart (astropy.Time): A time of interest or start time for a time 
                               range of interest
        tstop (astropy.Time, optional): The stop time for a time range of 
                                        interest.
    """
    _base_obs_finder = SwiftObsFinder
    
    def __init__(self, tstart, tstop=None):
        self.cd(tstart, tstop=tstop)
    
    @property
    def cwd(self):
        """(list): The current working directory for each observation ID"""
        return [finder.cwd for finder in self._finders]
    
    @property
    def files(self):
        """(list): The files that *might* contain data during the time or
        time range of interest"""
        files = []
        for finder in self._finders:
            files.extend(finder.files)
        return files
    
    @property
    def num_files(self):
        """(int): Number of files"""
        return len(self.files)
       
    def cd(self, tstart, tstop=None):
        """Changes the directories based on a time or time range of interest.
        
        Args:
            tstart (astropy.Time): A time of interest or start time for a time 
                                   range of interest
            tstop (astropy.Time, optional): The stop time for a time range of 
                                            interest.  
        """  
        if tstop is None:
            tstop = tstart
        
        self._tstart = tstart
        self._tstop = tstop
        
        # query the master catalog for the OBSIDs
        fpath = self._query_swift_master(tstart, tstop)
        obsids, tstarts = self._get_obsids_tstarts(fpath, tstart, tstop)
        num_dirs = len(obsids)
    
        # get the finders for each directory that *might* contain data at/over
        # the requested time
        self._finders = [self._base_obs_finder(tstarts[i], obsids[i]) \
                         for i in range(num_dirs)]
      
    def get(self, download_dir, files, verbose=True):
        """Downloads files to a directory and returns the downloaded file paths
        
        Args:
            download_dir (str): The download directory
            files (list): The list of files to download
            verbose (bool, optional): Set to False to turn off download status
        
        Returns:
            (list): The downloaded file paths
        """
        all_paths = []
        for finder in self._finders:
            for file in files:
                try:
                    path = finder.get(download_dir, [file], verbose=verbose)
                    all_paths.extend(path)
                except HTTPError:
                    # this just means the files don't exist in *this* directory
                    pass
                
        return all_paths
    
    def filter(self, filetype, extension):
        """Filters the directories for the requested filetype and extension

        Args:
            filetype (str): The type of file, e.g. 'cspec'
            extension (str): The file extension, e.g. '.pha'

        Returns:
            (list)
        """
        all_files = []
        for finder in self._finders:
            files = finder.filter(filetype, extension)
            all_files.extend(files)
        return all_files
        
    def _query_swift_master(self, tstart, tstop):
        """Queries the Swift Master catalog to figure out with observation IDs
        have data between `tstart` and `tstop`."""
        
        # construct the URL query
        host = 'https://heasarc.gsfc.nasa.gov'
        script = 'db-perl/W3Browse/w3query.pl'
        query = 'tablehead=name=heasarc_swiftmastr'
        query += '&varon=obsid&varon=start_time&sortvar=start_time' \
                 f'&bparam_start_time={quote(tstart.iso)}&varon=stop_time' \
                 f'&bparam_stop_time={quote(tstop.iso)}&'
        params = '&displaymode=FitsDisplay&ResultMax=0'
        url = f'{host}/{script}?{query}{params}'
        
        # submit query and write to a temp file
        context = ssl._create_unverified_context()
        page = urlopen(url, context=context)
        
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)
        
        fpath = os.path.join(cache_path, f'{tstart.isot}_{tstart.isot}.fit')
        with open(fpath, 'wb') as f:
            f.write(page.read())
        
        return fpath
    
    def _get_obsids_tstarts(self, fpath, tstart, tstop):
        """Return the observation IDs and tstarts from the Swift Master catalog
        dump.  This is complicated by the fact that HEASARC's query function is
        broken and returns observation IDs that are not contained within the 
        requested within the time range.
        """
        # open temp file, read, and delete file
        with fits.open(fpath) as f:
            obsids = f[1].data['OBSID']
            tstarts = f[1].data['START_TIME']
            tstops = f[1].data['STOP_TIME']
        os.remove(fpath)
        
        # reformat tstart and tstop
        tstarts = [float(t) for t in tstarts]
        tstops = [float(t) for t in tstops]
        
        # convert input tstart, tstop to MJD
        the_range = TimeRange(tstart.mjd, tstop.mjd)
        
        # HEASARC's query is broken in that it returns more rows than those that
        # contain the time range requested (hopefully it doesn't do the opposite.)
        # So we use TimeRange to see which rows overlap our time range.
        good_obsids = []
        good_tstarts = []
        for i in range(len(tstarts)):
            tr = TimeRange(tstarts[i], tstops[i])
            if TimeRange.intersection(the_range, tr) is not None:
                good_obsids.append(obsids[i])
                good_tstarts.append(tstarts[i])
        
        good_tstarts = Time(good_tstarts, format='mjd')
        
        return (good_obsids, good_tstarts)        

    def __repr__(self):
        tstart = self._tstart.iso
        tstop = self._tstop if self._tstop is None else self._tstop.iso
        return f'<{self.__class__.__name__}: {tstart}, {tstop}>' 


class SwiftAuxilTemporalFinder(SwiftTemporalFinder):
    """Find Swift auxiliary data that covers a given time or time range.
    
    See :class:`SwiftTemporalFinder` for details on how this class works.
    
    Parameters:
        tstart (astropy.Time): A time of interest or start time for a time 
                               range of interest
        tstop (astropy.Time, optional): The stop time for a time range of 
                                        interest.
    """
    _base_obs_finder = SwiftAuxilFinder
    
    def get_attitude(self, download_dir, which='best', **kwargs):
        """Download the spacecraft attitude (pointing) files.

        Args:
            download_dir (str): The download directory
            which (str): Which attitude files to return.  Options are 'all', 
                         'pat', 'sat', 'uat', and 'best'.  Default is 'best'.
                         The 'sat' attitude files are uncorrected/unsmoothed,
                         the 'pat' files are smoothed on ground, and the 'uat'
                         files are calibrated using UVOT observations (when 
                         available).  In terms of quality, uat > pat > sat, so
                         'best' returns the best available quality.
            verbose (bool, optional): If True, will output the download status.

        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_attitude(which=which), **kwargs)

    def get_orbit(self, download_dir, **kwargs):
        """Download the spacecraft orbit files.

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.

        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_orbit(), **kwargs)
    
    def ls_attitude(self, which='best'):
        """List the spacecraft attitude (pointing) files.
        
        Args:
            which (str): Which attitude files to return.  Options are 'all', 
                         'pat', 'sat', 'uat', and 'best'.  Default is 'best'.
                         The 'sat' attitude files are uncorrected/unsmoothed,
                         the 'pat' files are smoothed on ground, and the 'uat'
                         files are calibrated using UVOT observations (when 
                         available).  In terms of quality, uat > pat > sat, so
                         'best' returns the best available quality.
        
        Returns: 
            (list of str)
        """
        pat_files = self.filter('pat', 'fits.gz')
        sat_files = self.filter('sat', 'fits.gz')
        uat_files = self.filter('uat', 'fits.gz')
        
        if which == 'pat':
            return pat_files
        elif which == 'sat':
            return sat_files
        elif which == 'uat':
            return uat_files
        elif which == 'all':
            return pat_files + sat_files + uat_files
        elif which == 'best':
            if len(uat_files) > 0:
                return uat_files
            elif len(pat_files) > 0:
                return pat_files
            else:
                return sat_files
        else:
            raise ValueError(f'Incorrect attitude type: {which}')

    def ls_orbit(self):
        """List the Swift orbit files.
        
        Returns: 
            (list of str)
        """
        return self.filter('sao', 'fits.gz')
    
    
