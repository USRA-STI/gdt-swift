.. _gdt-swift:

****************************************************
Welcome to Swift Gamma-ray Data Tools Documentation!
****************************************************

.. figure:: images/swift_spacecraft.png

The Swift Gamma-ray Data Tools (GDT) is a toolkit for Swift-BAT data built on the
:external:ref:`GDT Core Package<gdt-core>` and is the next iteration of the
`Swift BAT Data Tools <https://swift.gsfc.nasa.gov/ssc/data/analysis/bat/bat_data_tools/gdt-docs>`_.

The Neil Gehrels Swift Observatory was launched on November 20, 2004 and contains
three intruments: the Burst Area Telescope (BAT), the X-ray Telescope (XRT) observing and the Ultraviolet/Optical Telescope (UVOT).
Currently the toolkit services all Swift BAT public data with a focus on the pipeline data products for Gamma-ray Bursts.

.. rubric:: Citing

If you use the Swift Gamma-ray Data Tools in your research and publications,
we would definitely appreciate an appropriate acknowledgment and citation! We
suggest the following BibTex:

::

 @misc{GDT-Swift,
       author = {Corinne Fletcher and Adam Goldstein and William H. Cleveland and Daniel Kocevski},
       title = {Swift Gamma-ray Data Tools: v1.0.0},
       year = 2023,
       url = {https://github.com/USRA-STI/gdt-Swift}
 }


.. rubric:: Additional Resources

The Swift Science Support Center is a fantastic resource for all things Swift found `here <https://swift.gsfc.nasa.gov/about_swift/ssc_services/>`_.  For
questions, bug reports, and comments, please visit the
`Swift Help Desk <https://swift.gsfc.nasa.gov/help/>`_.

.. rubric:: Acknowledgments

The creation of the Swift Gamma-ray Data Tools were funded by the NASA's Astrophysics Data Analysis Program (ADAP) via grant number 80NSSC21K0651.

***************
Getting Started
***************
.. toctree::
   :maxdepth: 1

   install

******************
User Documentation
******************

Swift Definitions
=================
.. toctree::
   :maxdepth: 1

   missions/swift/time
   missions/swift/frame



Swift BAT
=========

Instrument Definitions
----------------------

.. toctree::
   :maxdepth: 1


   missions/swift/bat/headers

Data Types
----------

.. toctree::
   :maxdepth: 1

   missions/swift/bat/pha
   missions/swift/bat/lightcurve
   missions/swift/bat/response
   missions/swift/bat/poshist


Data Finders and Catalogs
-------------------------

.. toctree::
   :maxdepth: 1

   missions/swift/bat/finders
   missions/swift/bat/catalogs

----

*******
License
*******
.. toctree::
   :maxdepth: 1

   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
