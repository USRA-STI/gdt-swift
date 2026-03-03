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
from ..finders import SwiftObsFinder, SwiftTemporalFinder
from ..time import *

__all__ = ['BatEventFinder', 'BatEventTemporalFinder', 
           'BatHousekeepingFinder','BatHousekeepingTemporalFinder', 
           'BatRateFinder', 'BatRateTemporalFinder',
           'BatSurveyFinder', 'BatSurveyTemporalFinder', 
           'BatTriggerFinder', 'BatTriggerTemporalFinder']


class BatEventFinder(SwiftObsFinder):
    """This class finds Swift BAT event data based on date and 
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
                            'bat', 'event')
        return path


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


class BatTriggerFinder(SwiftObsFinder):
    """This class finds Swift BAT triggered data based on date and observation 
    ID.
    
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
                            'bat', 'products')
        return path


class BatEventTemporalFinder(SwiftTemporalFinder):
    """Find Swift BAT event data that covers a given time or time range.
    
    See :class:`SwiftTemporalFinder` for details on how this class works.
    
    Parameters:
        tstart (astropy.Time): A time of interest or start time for a time 
                               range of interest
        tstop (astropy.Time, optional): The stop time for a time range of 
                                        interest.
    """
    _base_obs_finder = BatEventFinder

    def get_event(self, download_dir, **kwargs):
        """Download the event data files.

        Args:
            download_dir (str): The download directory
            verbose (bool, optional): If True, will output the download status.
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_event(), **kwargs)
    
    def ls_event(self):
        """List the event data files

        Returns:
            (list of str)
        """
        return self.filter('', 'evt.gz')


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


class BatTriggerTemporalFinder(SwiftTemporalFinder):
    """Find Swift BAT triggered data that covers a given time or time range.
    
    See :class:`SwiftTemporalFinder` for details on how this class works.
    
    Parameters:
        tstart (astropy.Time): A time of interest or start time for a time 
                               range of interest
        tstop (astropy.Time, optional): The stop time for a time range of 
                                        interest.
    """
    _base_obs_finder = BatTriggerFinder

    def get_afterslew(self, download_dir, **kwargs):
        """Download the afterslew files.
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_afterslew(), **kwargs)

    def get_all(self, download_dir, **kwargs):
        """Download all files.
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.files, **kwargs)
    
    def get_gti(self, download_dir, **kwargs):
        """Download the GTI data.
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_gti(), **kwargs)
    
    def get_lightcurve(self, download_dir, **kwargs):
        """Download the lightcurve data.
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_lightcurve(), **kwargs)

    def get_peak(self, download_dir, **kwargs):
        """Download the peak intensity files.
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_peak(), **kwargs)
    
    def get_preslew(self, download_dir, **kwargs):
        """Download the preslew files.
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_preslew(), **kwargs)
    
    def get_quicklook(self, download_dir, **kwargs):
        """Download the quicklook images (typically lightcurve and sky image).
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_quicklook(), **kwargs)

    def get_slew(self, download_dir, **kwargs):
        """Download the files during slew.
        
        Returns:
            (list): The file paths of the downloaded files
        """
        return self.get(download_dir, self.ls_slew(), **kwargs)
    
    def ls_afterslew(self):
        """List the after-slew files available.
        
        Returns:
            (list of str)
        """
        return self.filter('bevas', '')
    
    def ls_gti(self):
        """List the GTI files available.
        
        Returns:
            (list of str)
        """
        return self.filter('gti', '')
    
    def ls_lightcurve(self):
        """List the lightcurve data available.
        
        Returns:
            (list of str)
        """
        return self.filter('bev', 'lc.gz')

    def ls_peak(self):
        """List the files at peak intensity that are available.
        
        Returns:
            (list of str)
        """
        return self.filter('bevpb', '')
    
    def ls_preslew(self):
        """List the pre-slew files available.
        
        Returns:
            (list of str)
        """
        return self.filter('bevpb', '')
    
    def ls_quicklook(self):
        """List the quicklook images available (typically lightcurve and 
        sky image).
        
        Returns:
            (list of str)
        """
        return self.filter('', 'gif')

    def ls_slew(self):
        """List the files during slew that are available.
        
        Returns:
            (list of str)
        """
        return self.filter('bevsl', '')
