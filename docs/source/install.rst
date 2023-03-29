**********
Installing
**********

Installing with pip
===================
Try to install it with::

   pip install pyswmm

and an attempt will be made to find and install an appropriate version
that matches your operating system and Python version.

As of version 1.4.0, pyswmm can be installed with specific versions of the SWMM engine ranging from 5.1.14 to 5.2.3 using pip extras::

   pip install pyswmm["swmm5.2.1"]

SWMM and Python Compatibility
++++++++++++++++++++++++++++++
pyswmm has grown with EPA SWMM, supporting new versions as they are released. 
However, there are some compatibility limitations based on the version of pyswmm installed.

+----------------+-------------------------------------------------------+----------------------+
| pyswmm version | compatible swmm-toolkit versions (SWMM engine)        | python compatibility |
+================+=======================================================+======================+
| 1.0.0 - 1.1.1  | 0.8.2 (SWMM 5.1.13)                                   | 3.6 - 3.9            |
+----------------+-------------------------------------------------------+----------------------+
| 1.2.0 - 1.4.0  | | 0.9.1 - 0.14.0 (SWMM 5.1.14 - 5.2.3)                | 3.7 - 3.11           |
|                | | Note: 0.11.0 (SWMM 5.2.0) only supported on windows |                      |
+----------------+-------------------------------------------------------+----------------------+

.. attention::
   To use PySWMM you need 64-bit Python
