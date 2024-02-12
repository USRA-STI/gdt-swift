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

from gdt.core import cache_path
from gdt.core.heasarc import BrowseCatalog

__all__ = ['GrbCatalog', 'MasterCatalog']

bat_cache_path = os.path.join(cache_path, 'swiftbat')
print(bat_cache_path)
class GrbCatalog(BrowseCatalog):
    """Class that interfaces with the GBM Trigger Catalog via HEASARC Browse.

    Note:
        Because this calls HEASARC's w3query.pl script on initialization,
        it may take several seconds for the object to load.

    Parameters:
        cache_path (str): The path where the cached catalog will live.
        cached (bool, optional): Set to True to read from the cached file
                                 instead of querying HEASARC. Default is False.
        verbose (bool, optional): Default is True

    Attributes:
        columns (np.array): The names of the columns available in the table
        num_cols (int): The total number of columns (fields) in the data table
        num_rows: (int): The total number of rows in the data table
    """
    def __init__(self, cache_path=bat_cache_path, **kwargs):
        super().__init__(cache_path, table='swiftgrb', **kwargs)

class MasterCatalog(BrowseCatalog):
    """Class that interfaces with the GBM Burst Catalog via HEASARC Browse.

    Note:
        Because this calls HEASARC's w3query.pl script on initialization,
        it may take several seconds up to a couple of minutes for the object
        to load.

    Parameters:
        cache_path (str): The path where the cached catalog will live.
        cached (bool, optional): Set to True to read from the cached file
                                 instead of querying HEASARC. Default is False.
        verbose (bool, optional): Default is True

    Attributes:
        columns (np.array): The names of the columns available in the table
        num_cols (int): The total number of columns (fields) in the data table
        num_rows: (int): The total number of rows in the data table
    """
    def __init__(self, cache_path=bat_cache_path, **kwargs):
        super().__init__(cache_path, table='swiftmastr', **kwargs)
