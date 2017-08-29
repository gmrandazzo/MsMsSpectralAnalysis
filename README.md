# MsMsSpectralAnalysis

Create/Edit/Modify/Analyze MSP and MGF files.


![ScreenShot](https://github.com/gmrandazzo/MsMsSpectralAnalysis/blob/master/mspfm.png)


Standard fields
===============
MGF and MSP files are standardised according these fields:

- Name: compound name
- SMILES: molecular structure
- PRECURSORMZ: m/z precursor ion
- INSTRUMENT: instrumental brand (Waters Xevo, Thermo Orbitrap, etc..)
- INSTRUMENTTYPE: type of the instrument (ESI-LC-MS etc..)
- COLLISIONENERGY: energy of collision with fragmentation type (CID 20, HCD 30 etc..)
- RETENTIONTIME: retention time (min)
- IONMODE: positive or negative
- BIOLOGICALSOURCE: human blood, rat urine, cell H295R, plant Plectranthus barbatus, etc...
- LINKS: CAS number, HMDB ID, LipidMaps ID etc..


License
============

PyLSS is distributed under LGPLv3 license, this means that:

- you can use this library where you want doing what you want.
- you can modify this library and commit changes.
- you can not use this library inside a commercial software.

To know more in details how the licens work please read the file "LICENSE" or
go to "http://www.gnu.org/licenses/lgpl-3.0.html"

PyLSS is currently property of Giuseppe Marco Randazzo which is also the
current package maintainer.

Voluntary contributions are welcome.



Dependencies
============

The required dependencies to use PyLSS are:

- python version 3
- matplotlib
- PyQt5
- pathlib



Developper
=========

MsMsSpectralAnalysis is written and mantained by Giuseppe Marco Randazzo <gmrandazzo@gmail.com>

