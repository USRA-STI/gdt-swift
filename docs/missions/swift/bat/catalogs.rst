.. _bat-catalogs:

***********************************************************
swift bat Catalogs (:mod:`gdt.missions.swift.bat.catalogs`)
***********************************************************

The HEASARC hosts two main BAT catalogs: a GRB Catalog that contains
information and original data products about every GRB observed by BAT and a Master Catalog that contains high level data for each observation performed by BAT. HEASARC provides a way to search these
catalogs online through their Browse interface, but we offer a way to do it in
Python through the Data Tools. Currently the Data tools only supports the BAT GRB Catalog but will add the Master Catalog at a later date.

Let's look at the trigger catalog first:

    >>> from gdt.missions.swift.bat.catalogs import GrbCatalog
    >>> grbcat = GrbCatalog()
    Sending request and awaiting response from HEASARC...
    Downloading swiftgrb from HEASARC via w3query.pl...
    Finished in 10 s
    >>> grbcat
    <GrbCatalog: 178 columns, 872 rows>

Depending on your connection, initialization may take a few seconds. You can
see what columns are available in the catalog:

    >>> print(grbcat.columns)
    ('NAME', 'TARGET_ID', 'RA', 'DEC', ....., 'XRT_POS_ERR', 'XRT_POS_REF', 'XRT_RA')


You can also return the range of values for a given column:

    >>> grbcat.column_range('NAME')
    ('GRB 041217  ', 'GRB 121229A ')

If you only care about specific columns in the table, you can return a numpy
record array with only those columns. Let's return a table with the trigger
name and time for every trigger:

    >>> grbcat.get_table(columns=('NAME', 'TRIGGER_TIME'))
    rec.array([('GRB 041217  ', '2004-12-17T07:28:25.920000'),
           ('GRB 041218  ', '2004-12-18T15:45:25       '),
           ('GRB 041219A ', '2004-12-19T01:42:18.000000'),
           ('GRB 041219B ', '2004-12-19T15:38:48.000000'),
           ('GRB 041219C ', '2004-12-19T20:30:34.000000'), ....
           ('GRB 121226A ', '2012-12-26T19:09:43       '),
           ('GRB 121229A ', '2012-12-29T05:00:21       ')],
          dtype=[('NAME', '<U12'), ('TRIGGER_TIME', '<U26')])

Importantly, we can make slices of the catalog based on conditionals. Let's
only select GRBs with localization radii between 0.0 and 1.0 degrees:

    >>> sliced_grbcat = grbcat.slice('POS_ERR', lo=0., hi=1.0)
    >>> sliced_grbcat
    <GrbCatalog: 178 columns, 425 rows>

    >>> sliced_grbcat.get_table(columns=('NAME', 'TRIGGER_TIME'))
    rec.array([('GRB 041219A ', '2004-12-19T01:42:18.000000'),
           ('GRB 041219B ', '2004-12-19T15:38:48.000000'),
           ('GRB 041223  ', '2004-12-23T14:06:17.956380'), ....
           ('GRB 121212A ', '2012-12-12T06:56:13       '),
           ('GRB 121217A ', '2012-12-17T07:17:47       '),
           ('GRB 121226A ', '2012-12-26T19:09:43       '),
           ('GRB 121229A ', '2012-12-29T05:00:21       ')],
          dtype=[('NAME', '<U12'), ('TRIGGER_TIME', '<U26')])

You can also slice on multiple conditionals, simultaneously. Select everything
that has a localization radius between 0.0-1.0 degrees, *and* a duration between 0.0-2.0 seconds:

    >>> sliced_grbcat2 = grbcat.slices([('POS_ERR', 0.0, 1.0),
    >>>                                   ('DURATION', 0.0, 2.0)])
    >>> sliced_grbcat2
    <GrbCatalog: 178 columns, 121 rows>

    >>> sliced_grbcat2.get_table(columns=('NAME', 'TRIGGER_TIME', 'POS_ERR'))
    rec.array([('GRB 041219A ', '2004-12-19T01:42:18.000000', 0. ),
           ('GRB 041219B ', '2004-12-19T15:38:48.000000', 0. ),
           ('GRB 041223  ', '2004-12-23T14:06:17.956380', 0.2),
           ('GRB 080507  ', '2008-05-07T07:45:00       ', 0.7), ...
           ('GRB 121212A ', '2012-12-12T06:56:13       ', 0.3),
           ('GRB 121226A ', '2012-12-26T19:09:43       ', 0.2),
           ('GRB 121229A ', '2012-12-29T05:00:21       ', 0.5)],
          dtype=[('NAME', '<U12'), ('TRIGGER_TIME', '<U26'), ('POS_ERR', '<f8')])


For more information on working with catalogs, see
:external:ref:`The BrowseCatalog Class<core-heasarc-browse>`.

Reference/API
=============

.. automodapi:: gdt.missions.swift.bat.catalogs
   :inherited-members:
