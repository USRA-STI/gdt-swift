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
from ..time import *

__all__ = ['BatDataProductsFtp', 'BatAuxiliaryFtp']

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

    def cd(self):
        """Change directory to obsid number.

        Args:
            obsid (str): A valid observation ID number
            date (str): a date (YYYY-MM) for the observation
        """

        super().cd(self)

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

    def get_lightcurve(self, download_dir,*args, **kwargs):
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

    def get_gti(self, download_dir,*args, **kwargs):
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

    def get_response(self, download_dir,*args, **kwargs):
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

    def get_pha(self, download_dir,*args, **kwargs):
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

    def get_preslew(self, download_dir,*args, **kwargs):
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

    def get_slew(self, download_dir,*args, **kwargs):
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

    def get_afterslew(self, download_dir,*args, **kwargs):
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
        path = os.path.join(self._root, year + '_' + day,  obsid +'000', 'bat', 'products')

        try:
            trigger_dirs = self._ftp.nlst(path)
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

    def get_sao(self, download_dir,*args, **kwargs):
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

    def get_sat(self, download_dir,*args, **kwargs):
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
        path = os.path.join(self._root, year + '_' + day,  obsid +'000', 'auxil')

        try:
            trigger_dirs = self._ftp.nlst(path)
        except:
            raise FileExistsError

        return path
