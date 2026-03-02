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
import os
from math import floor
from gdt.core.heasarc import FtpFinder
from ..finders import SwiftObsFinder, SwiftTemporalFinder
from ..time import *

__all__ = ['BatHousekeepingFinder', 'BatRateFinder', 'BatRateTemporalFinder',
           'BatSurveyFinder', 'BatHousekeepingTemporalFinder',
           'BatSurveyTemporalFinder', 'BatDataProductsFtp', 'BatAuxiliaryFtp']


class BatHousekeepingFinder(SwiftObsFinder):
    """This class finds Swift BAT housekeeping data based on date and 
    observation ID.
    
    Parameters:
        date (astropy.Time, optional): A time for the observation
        obsid (str, optional): A valid observation ID number
    """
    def _construct_path(self, date, obsid):
        """Constructs the FTP path for a observation

        Args:
            date (astropy.Time): The date/time
            obsid (str): The observation ID

        Returns:
            str: The path of the FTP directory for the observation
        """
        path = os.path.join(self._root, date.utc.strftime('%Y_%m'), obsid, 
                            'bat', 'hk')
        return path



class BatRateFinder(SwiftObsFinder):
    """This class finds Swift BAT rate data based on date and observation ID.
    
    Parameters:
        date (astropy.Time, optional): A time for the observation
        obsid (str, optional): A valid observation ID number
    """
    def _construct_path(self, date, obsid):
        """Constructs the FTP path for a observation

        Args:
            date (astropy.Time): The date/time
            obsid (str): The observation ID

        Returns:
            str: The path of the FTP directory for the observation
        """
        path = os.path.join(self._root, date.utc.strftime('%Y_%m'), obsid, 
                            'bat', 'rate')
        return path


class BatSurveyFinder(SwiftObsFinder):
    """This class finds Swift BAT survey data based on date and observation ID.
    
    Parameters:
        date (astropy.Time, optional): A time for the observation
        obsid (str, optional): A valid observation ID number
    """
    def _construct_path(self, date, obsid):
        """Constructs the FTP path for a observation

        Args:
            date (astropy.Time): The date/time
            obsid (str): The observation ID

        Returns:
            str: The path of the FTP directory for the observation
        """
        path = os.path.join(self._root, date.utc.strftime('%Y_%m'), obsid, 
                            'bat', 'survey')
        return path


class BatHousekeepingTemporalFinder(SwiftTemporalFinder):
    """Find Swift BAT housekeeping data that covers a given time or time range.
    
    See :class:`SwiftTemporalFinder` for details on how this class works.
    
    Parameters:
        tstart (astropy.Time): A time of interest or start time for a time 
                               range of interest
        tstop (astropy.Time, optional): The stop time for a time range of 
                                        interest.
    """
    _base_obs_finder = BatHousekeepingFinder

    def get_det_enabled(self, download_dir, **kwargs):
        """Download the files containing the map of enabled BAT detectors.

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_det_enabled(), **kwargs)

    def get_gain_offset(self, download_dir, **kwargs):
        """Download the files containing the gain and offset of the BAT detectors.

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_gain_offset(), **kwargs)

    def ls_det_enabled(self):
        """List the files containing the map of enabled BAT detectors.

        Returns:
            (list of str)
        """
        return self.filter('decb', 'hk.gz')

    def ls_gain_offset(self):
        """List the files containing the gain and offset of the BAT detectors.

        Returns:
            (list of str)
        """
        return self.filter('bgoc', 'hk.gz')
    

class BatRateTemporalFinder(SwiftTemporalFinder):
    """Find Swift BAT rate data that covers a given time or time range.
    
    See :class:`SwiftTemporalFinder` for details on how this class works.
    
    Parameters:
        tstart (astropy.Time): A time of interest or start time for a time 
                               range of interest
        tstop (astropy.Time, optional): The stop time for a time range of 
                                        interest.
    """
    _base_obs_finder = BatRateFinder

    def get_millisecond_lc(self, download_dir, **kwargs):
        """Download the millisecond lightcurve data.

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_millisecond_lc(), **kwargs)

    def get_multichannel_lc(self, download_dir, **kwargs):
        """Download the multi-channel lightcurve data.

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.

        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_multichannel_lc(), **kwargs)

    def get_quadrant_lc(self, download_dir, **kwargs):
        """Download the lightcurve data split into observing quadrants.

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.

        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_quadrant_lc(), **kwargs)

    def get_second_lc(self, download_dir, **kwargs):
        """Download the 1-second resolution lightcurve.

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.

        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_second_lc(), **kwargs)

    def ls_millisecond_lc(self):
        """List the millisecond lightcurve data files.

        Returns:
            (list of str)
        """
        return self.filter('brtms', 'lc.gz')
    
    def ls_multichannel_lc(self):
        """List the multi-channel lightcurve data files.

        Returns:
            (list of str)
        """
        return self.filter('brtmc', 'lc.gz')

    def ls_quadrant_lc(self):
        """List the quadrant lightcurve data files.

        Returns:
            (list of str)
        """
        return self.filter('brtqd', 'lc.gz')

    def ls_second_lc(self):
        """List the 1-second resolution lightcurve data files.

        Returns:
            (list of str)
        """
        return self.filter('brt1s', 'lc.gz')


class BatSurveyTemporalFinder(SwiftTemporalFinder):
    """Find Swift BAT survey data that covers a given time or time range.
    
    See :class:`SwiftTemporalFinder` for details on how this class works.
    
    Parameters:
        tstart (astropy.Time): A time of interest or start time for a time 
                               range of interest
        tstop (astropy.Time, optional): The stop time for a time range of 
                                        interest.
    """
    _base_obs_finder = BatSurveyFinder
    
    def get_survey(self, download_dir, **kwargs):
        """Download the survey detector plane histogram files.

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.

        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_survey(), **kwargs)
    
    def ls_survey(self):
        """List the survey detector plane histogram files.
        
        Returns: 
            (list of str)
        """
        return self.filter('bsv', 'dph.gz')
    
    
    
#####

class BatFinder(FtpFinder):
    """Subclassing FtpFinder to enable _file_filter() to take a list
    """

    def _file_filter(self, file_list, filetype, extension):
        """Filters the directory for the requested filetype, and extension

        Args:
            filetype (str): The type of file, e.g. 'cont'
            extension (str): The file extension, e.g. '.fit'

        Returns:
            (list): The filtered file list
        """
        files = super()._file_filter(file_list, filetype, extension)

        return files


class BatDataProductsFtp(BatFinder):
    """A class that interfaces with the HEASARC FTP directories.
    An instance of this class will represent the available files associated
    with a single event.

    An instance can be created with an observation ID and a date (YYYY-MM) to query and download files.
    An instance can also be changed from one trigger number to another without
    having to create a new instance.  If multiple instances are created and
    exist simultaneously, they will all use a single FTP connection.

    Parameters:
        obsid (str, optional): A valid observation ID number
        date (str, optional): a date (YYYY-MM) for the observation

    Attributes:
        num_files (int): Number of files in the current directory
        files (list of str): The list of files in the current directory
    """
    _root = '/swift/data/obs/'

    def _validate(self, obsid, date):
        return super()._validate(obsid, date)

    def cd(self, obsid: str, date: str):
        """Change directory to obsid number.

        Args:
            obsid (str): A valid observation ID number
            date (str): a date (YYYY-MM) for the observation
        """
        super().cd(obsid, date)


    def get_all(self, download_dir, **kwargs):
        """Download all files within a data products directory.

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
                                      Default is True.
        """
        return self.get(download_dir, self._file_list, **kwargs)


    def ls_all(self):
        """List all files for the observations data products

        Returns:
            (list of str)

        """
        return self._file_filter(self.files, '', '')


    def ls_lightcurve(self):
        """List all lightcurve data for the observation

        Returns:
            (list of str)
        """

        files = []
        files.extend(self._file_filter(self.files, 'lc', ''))
        return files


    def get_lightcurve(self, download_dir, *args, **kwargs):
        """Download the lightcurve data for the observation

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
                                      Default is True.
        """
        files = self._file_filter(self.files, 'lc', '')
        self.get(download_dir, files, **kwargs)


    def ls_gti(self):
        """List all good timing interval data for the observation

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, '', 'gti.gz')


    def get_gti(self, download_dir, *args, **kwargs):
        """Download the good timing interval data for the observation

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
                                      Default is True.
        """
        files = self._file_filter(self.files, '', 'gti.gz')
        self.get(download_dir, files, **kwargs)


    def ls_response(self):
        """List all response files for the observation

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, '', 'rsp.gz')


    def get_response(self, download_dir, *args, **kwargs):
        """Download the response files for the observation

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
                                      Default is True.
        """
        files = self._file_filter(self.files, '', 'rsp.gz')
        self.get(download_dir, files, **kwargs)


    def ls_pha(self):
        """List all pha files for the observation

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, '', 'pha.gz')


    def get_pha(self, download_dir, *args, **kwargs):
        """Download the pha files for the observation

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
                                      Default is True.
        """
        files = self._file_filter(self.files, '', 'pha.gz')
        self.get(download_dir, files, **kwargs)


    def ls_preslew(self):
        """List all pre-slew files for the observation

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'bevps', '')


    def get_preslew(self, download_dir, *args, **kwargs):
        """Download the pre-slew files for the observation

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
                                      Default is True.
        """
        files = self._file_filter(self.files, 'bevps', '')
        self.get(download_dir, files, **kwargs)


    def ls_slew(self):
        """List all files during slew for the observation

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'bevsl', '')


    def get_slew(self, download_dir, *args, **kwargs):
        """Download the files during slew for the observation

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
                                      Default is True.
        """
        files = self._file_filter(self.files, 'bevsl', '')
        self.get(download_dir, files, **kwargs)


    def ls_afterslew(self):
        """List all after-slew files for the observation

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'bevas', '')


    def get_afterslew(self, download_dir, *args, **kwargs):
        """Download the after-slew for the observation

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
                                      Default is True.
        """
        files = self._file_filter(self.files, 'bevas', '')
        self.get(download_dir, files, **kwargs)


    def _construct_path(self, obsid, date):
        """Constructs the FTP path for a observation

        Args:
            obsid (str): The observation ID
            date (str): given in YYYY-MM

        Returns:
            str: The path of the FTP directory for the observation
        """

        year = date[:4]
        day = date[5:]
        path = os.path.join(self._root, year + '_' + day, obsid + '000', 'bat', 'products')

        try:
            trigger_dirs = self._protocol.ls(path)
        except:
            raise FileExistsError

        return path


class BatAuxiliaryFtp(BatFinder):
    """A class that interfaces with the HEASARC FTP observation auxiliary directories.
    An instance of this class will represent the available files associated
    with an the observation.

    An instance can be created with an observation ID and a date (YYYY-MM) to query and download files.
    An instance can also be changed from one trigger number to another without
    having to create a new instance.  If multiple instances are created and
    exist simultaneously, they will all use a single FTP connection.

    Parameters:
        obsid (str, optional): A valid observation ID number
        date (str, optional): a date (YYYY-MM) for the observation

    Attributes:
        num_files (int): Number of files in the current directory
        files (list of str): The list of files in the current directory
    """
    _root = '/swift/data/obs/'

    def ls_all(self):
        """List all files for the observation

        Returns:
            (list of str)

        """
        return self._file_filter(self.files, '', '')

    def get_all(self, download_dir, **kwargs):
        """Download all files within a data products observation.

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
                                      Default is True.
        """
        self.get(download_dir, self._file_list, **kwargs)

    def ls_sao(self):
        """List SAO file for the observation

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'sao', '.')

    def get_sao(self, download_dir, *args, **kwargs):
        """Download the SAO file for the observation

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
                                      Default is True.
        """
        files = self._file_filter(self.files, 'sao', '')
        self.get(download_dir, files, **kwargs)

    def ls_sat(self):
        """List the SAT file for the observation

        Returns:
            (list of str)
        """
        return self._file_filter(self.files, 'sat', '.')

    def get_sat(self, download_dir, *args, **kwargs):
        """Download SAT File for the observation

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
                                      Default is True.
        """
        files = self._file_filter(self.files, 'sat', '')
        self.get(download_dir, files, **kwargs)

    def _construct_path(self, obsid, date):
        """Constructs the FTP path for a observation

        Args:
            obsid (str): The observation ID
            date (str): given in YYYY-MM

        Returns:
            str: The path of the FTP directory for the trigger
        """

        year = date[:4]
        day = date[5:]
        path = os.path.join(self._root, year + '_' + day, obsid + '000', 'auxil')

        try:
            trigger_dirs = self._protocol.ls(path)
        except:
            raise FileExistsError

        return path
