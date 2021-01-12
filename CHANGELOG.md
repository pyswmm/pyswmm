# History of changes

## Version 1.0.0 (2021-01-12)

### Issues Closed

#### Enhancements

* [Issue 264](https://github.com/OpenWaterAnalytics/pyswmm/issues/264) - Refactor PySWMM to use swmm-toolkit package ([PR 262](https://github.com/OpenWaterAnalytics/pyswmm/pull/262))

#### Maintenance

* [Issue 265](https://github.com/OpenWaterAnalytics/pyswmm/issues/265) - Repository clean up ([PR 262](https://github.com/OpenWaterAnalytics/pyswmm/pull/262))

#### Deprecated

* [Issue 263](https://github.com/OpenWaterAnalytics/pyswmm/issues/263) - Deprecate DLL selector function ([PR 262](https://github.com/OpenWaterAnalytics/pyswmm/pull/262))

In this release 3 issues were closed.

### Pull Requests Merged

* [PR 262](https://github.com/OpenWaterAnalytics/pyswmm/pull/262) - PySWMM v1.0 ([265](https://github.com/OpenWaterAnalytics/pyswmm/issues/265), [264](https://github.com/OpenWaterAnalytics/pyswmm/issues/264), [263](https://github.com/OpenWaterAnalytics/pyswmm/issues/263))

In this release 1 pull request was closed.


## Version 0.6.2 (2020/08/04)

Updating release version.

## Version 0.6.1 (2020/08/04)


### Pull Requests Merged

* [PR 217](https://github.com/OpenWaterAnalytics/pyswmm/pull/217) - add node, link water quality getters, by [@katmratliff](https://github.com/katmratliff) ([206](https://github.com/OpenWaterAnalytics/pyswmm/issues/206))

In this release 1 pull request was closed.

## Version 0.6.0 (2019-10-19)


### Pull Requests Merged

* [PR 214](https://github.com/OpenWaterAnalytics/pyswmm/pull/214) - Feat terminate sim ([213](https://github.com/OpenWaterAnalytics/pyswmm/issues/213))

In this release 1 pull request was closed.

## Version 0.5.2 (2019-10-08)


### Pull Requests Merged

* [PR 212](https://github.com/OpenWaterAnalytics/pyswmm/pull/212) - change single ptr struct to double ptr struct for ctypes for subcatch ([211](https://github.com/OpenWaterAnalytics/pyswmm/issues/211))
* [PR 208](https://github.com/OpenWaterAnalytics/pyswmm/pull/208) - update SWMM5 libraries compiled with optimizer flags ([209](https://github.com/OpenWaterAnalytics/pyswmm/issues/209))

In this release 2 pull requests were closed.

## Version 0.5.1 (2019/08/26)

### Pull Requests Merged

* [PR 208](https://github.com/OpenWaterAnalytics/pyswmm/pull/208) - update SWMM5 libraries compiled with optimizer flags ([209](https://github.com/OpenWaterAnalytics/pyswmm/issues/209))

In this release 1 pull request was closed.

## Version 0.5.0 (2019/07/26)

### Issues Closed

#### New Features

* [Issue 199](https://github.com/OpenWaterAnalytics/pyswmm/issues/199) - Add support to RainGage API ([PR 198](https://github.com/OpenWaterAnalytics/pyswmm/pull/198))
* [Issue 194](https://github.com/OpenWaterAnalytics/pyswmm/issues/194) - Add LID support to pyswmm  ([PR 152](https://github.com/OpenWaterAnalytics/pyswmm/pull/152))

#### Bugs fixed

* [Issue 192](https://github.com/OpenWaterAnalytics/pyswmm/issues/192) - latest version of v0.4.9.dev0 seems unstable ([PR 152](https://github.com/OpenWaterAnalytics/pyswmm/pull/152))
* [Issue 172](https://github.com/OpenWaterAnalytics/pyswmm/issues/172) - `error_check` swallows exceptions and converts them to warnings ([PR 173](https://github.com/OpenWaterAnalytics/pyswmm/pull/173))
* [Issue 164](https://github.com/OpenWaterAnalytics/pyswmm/issues/164) - pump_statistics['max_flowrate'] gives zero division error ([PR 204](https://github.com/OpenWaterAnalytics/pyswmm/pull/204))
* [Issue 146](https://github.com/OpenWaterAnalytics/pyswmm/issues/146) - Fix linux / osx CI

In this release 6 issues were closed.

### Pull Requests Merged

* [PR 204](https://github.com/OpenWaterAnalytics/pyswmm/pull/204) - Bug Fix Issue 164 ([164](https://github.com/OpenWaterAnalytics/pyswmm/issues/164))
* [PR 203](https://github.com/OpenWaterAnalytics/pyswmm/pull/203) - Merge develop to master ([201](https://github.com/OpenWaterAnalytics/pyswmm/issues/201), [200](https://github.com/OpenWaterAnalytics/pyswmm/issues/200))
* [PR 198](https://github.com/OpenWaterAnalytics/pyswmm/pull/198) - Merging Abhi's Raingage API work ([199](https://github.com/OpenWaterAnalytics/pyswmm/issues/199), [155](https://github.com/OpenWaterAnalytics/pyswmm/issues/155))
* [PR 191](https://github.com/OpenWaterAnalytics/pyswmm/pull/191) - Eliminating VCOMP DLL Not Found on Windows ([186](https://github.com/OpenWaterAnalytics/pyswmm/issues/186), [153](https://github.com/OpenWaterAnalytics/pyswmm/issues/153))
* [PR 175](https://github.com/OpenWaterAnalytics/pyswmm/pull/175) - doc update simulation to sim
* [PR 173](https://github.com/OpenWaterAnalytics/pyswmm/pull/173) - Make _error_check throw exception for all errcodes ([172](https://github.com/OpenWaterAnalytics/pyswmm/issues/172))
* [PR 170](https://github.com/OpenWaterAnalytics/pyswmm/pull/170) - add getters for pollutant surface buildup and ponded concentration in subcatchments
* [PR 165](https://github.com/OpenWaterAnalytics/pyswmm/pull/165) - Simple ci ([166](https://github.com/OpenWaterAnalytics/pyswmm/issues/166))
* [PR 163](https://github.com/OpenWaterAnalytics/pyswmm/pull/163) - Update system.py docs ([162](https://github.com/OpenWaterAnalytics/pyswmm/issues/162))
* [PR 154](https://github.com/OpenWaterAnalytics/pyswmm/pull/154) - Updated Linux Binary ([133](https://github.com/OpenWaterAnalytics/pyswmm/issues/133))
* [PR 152](https://github.com/OpenWaterAnalytics/pyswmm/pull/152) - LID Support ([197](https://github.com/OpenWaterAnalytics/pyswmm/issues/197), [196](https://github.com/OpenWaterAnalytics/pyswmm/issues/196), [194](https://github.com/OpenWaterAnalytics/pyswmm/issues/194), [192](https://github.com/OpenWaterAnalytics/pyswmm/issues/192))
* [PR 151](https://github.com/OpenWaterAnalytics/pyswmm/pull/151) - Updated Node Tests with Assertion Checks ([150](https://github.com/OpenWaterAnalytics/pyswmm/issues/150))
* [PR 109](https://github.com/OpenWaterAnalytics/pyswmm/pull/109) - Adding Code of Conduct to Project

In this release 13 pull requests were closed.

## Version 0.4.7 (2018-01-08)

### Issues Closed

#### New Features

* [Issue 147](https://github.com/OpenWaterAnalytics/pyswmm/issues/147) - Add before_end simulation hook.

In this release 1 issue was closed.

### Pull Requests Merged

* [PR 148](https://github.com/OpenWaterAnalytics/pyswmm/pull/148) - Added additional callback hook for Before_End

In this release 1 pull request was closed.

## Version 0.4.6 (2018-01-02)

### Issues Closed

#### New Features

* [Issue 140](https://github.com/OpenWaterAnalytics/pyswmm/issues/140) - Add simulation function hook for callbacks

#### Bugs fixed

* [Issue 143](https://github.com/OpenWaterAnalytics/pyswmm/issues/143) - Remove bare exceptions

In this release 2 issues were closed.

### Pull Requests Merged

* [PR 144](https://github.com/OpenWaterAnalytics/pyswmm/pull/144) - Added swmm_lib_path argument to Simulation and PySWMM class
* [PR 142](https://github.com/OpenWaterAnalytics/pyswmm/pull/142) - Added Hooks for Callbacks

In this release 2 pull requests were closed.

## Version 0.4.5 (2017-12-27)

### Issues Closed

#### New Features

* [Issue 90](https://github.com/OpenWaterAnalytics/pyswmm/issues/90) - Add test *.inp files to distribution

#### Bugs fixed

* [Issue 139](https://github.com/OpenWaterAnalytics/pyswmm/issues/139) - Update SWMM5 Lib Windows - Linking Issue
* [Issue 136](https://github.com/OpenWaterAnalytics/pyswmm/issues/136) - broken doctests

In this release 3 issues were closed.

## Version 0.4.4 (2017-11-14)

### Issues Closed

#### New Features

* [Issue 127](https://github.com/OpenWaterAnalytics/pyswmm/issues/127) - Set Outfall Stage  ([PR 128](https://github.com/OpenWaterAnalytics/pyswmm/pull/128))
* [Issue 125](https://github.com/OpenWaterAnalytics/pyswmm/issues/125) - pollutant buildup addition to subcatchment stats

In this release 2 issues were closed.

### Pull Requests Merged

* [PR 129](https://github.com/OpenWaterAnalytics/pyswmm/pull/129) - Add subcatchment surface buildup to subcatchment statistics
* [PR 128](https://github.com/OpenWaterAnalytics/pyswmm/pull/128) - Set bc ([127](https://github.com/OpenWaterAnalytics/pyswmm/issues/127))

In this release 2 pull requests were closed.

## Version 0.4.2 (2017-08-24)

### Issues Closed

#### Bugs fixed

* [Issue 119](https://github.com/OpenWaterAnalytics/pyswmm/issues/119) - Update SWMM Library
* [Issue 115](https://github.com/OpenWaterAnalytics/pyswmm/issues/115) - execute() method

In this release 2 issues were closed.

## Version 0.4.1 (2017-08-09)


### Pull Requests Merged

* [PR 113](https://github.com/OpenWaterAnalytics/pyswmm/pull/113) - Bug Fixes

In this release 1 pull request was closed.

## Version 0.4.0 (2017-07-14)


### Pull Requests Merged

* [PR 106](https://github.com/OpenWaterAnalytics/pyswmm/pull/106) - Updatetests
* [PR 103](https://github.com/OpenWaterAnalytics/pyswmm/pull/103) - Linux
* [PR 97](https://github.com/OpenWaterAnalytics/pyswmm/pull/97) - Statsfix

In this release 3 pull requests were closed.

## Version 0.3.4 (2017-05-08)


### Pull Requests Merged

* [PR 89](https://github.com/OpenWaterAnalytics/pyswmm/pull/89) - added Simulation.percent_complete property and fixed function name

In this release 1 pull request was closed.


## Version 0.3.3 (2017/05/05)


### Pull Requests Merged

* [PR 86](https://github.com/OpenWaterAnalytics/pyswmm/pull/86) - Support for SWMM 5.1.12 and exposed error and engine version properties
* [PR 81](https://github.com/OpenWaterAnalytics/pyswmm/pull/81) - Python 3 Support

In this release 2 pull requests were closed.


## Version 0.3.2 (2017/03/13)


### Pull Requests Merged

* [PR 78](https://github.com/OpenWaterAnalytics/pyswmm/pull/78) - added SWMM5 engine selector

In this release 1 pull request was closed.

## Version 0.3.1 (2017/03/10)


### Pull Requests Merged

* [PR 76](https://github.com/OpenWaterAnalytics/pyswmm/pull/76) - re-compiled SWMM to fix set simulation time functions
* [PR 73](https://github.com/OpenWaterAnalytics/pyswmm/pull/73) - updated default save to bin file
* [PR 70](https://github.com/OpenWaterAnalytics/pyswmm/pull/70) - PR: Update readme

In this release 3 pull requests were closed.


## Version 0.3 (2017/02/24)

### Issues Closed

#### New Features

* [Issue 63](https://github.com/OpenWaterAnalytics/pyswmm/issues/63) - updates to Simulation.py
* [Issue 27](https://github.com/OpenWaterAnalytics/pyswmm/issues/27) - Enhancements to pyswmm.Simulation base classes

#### Bugs fixed

* [Issue 55](https://github.com/OpenWaterAnalytics/pyswmm/issues/55) - import update bug fix for py2.7
* [Issue 48](https://github.com/OpenWaterAnalytics/pyswmm/issues/48) - Fix Docs

In this release 4 issues were closed.

### Pull Requests Merged

* [PR 69](https://github.com/OpenWaterAnalytics/pyswmm/pull/69) - hot fix - subcatchments
* [PR 68](https://github.com/OpenWaterAnalytics/pyswmm/pull/68) - PR: Fix code style
* [PR 67](https://github.com/OpenWaterAnalytics/pyswmm/pull/67) - added subcatchments.py module
* [PR 66](https://github.com/OpenWaterAnalytics/pyswmm/pull/66) - turned off reader module
* [PR 62](https://github.com/OpenWaterAnalytics/pyswmm/pull/62) - Updated Simulation Docs and Added Current Time Function
* [PR 61](https://github.com/OpenWaterAnalytics/pyswmm/pull/61) - PR: Report coverage
* [PR 58](https://github.com/OpenWaterAnalytics/pyswmm/pull/58) - PR: Fix/ci
* [PR 57](https://github.com/OpenWaterAnalytics/pyswmm/pull/57) - Updates to docs
* [PR 56](https://github.com/OpenWaterAnalytics/pyswmm/pull/56) - Fix import for py2.7
* [PR 53](https://github.com/OpenWaterAnalytics/pyswmm/pull/53) - #48 Updates to docs
* [PR 49](https://github.com/OpenWaterAnalytics/pyswmm/pull/49) - Bug Fix All API Enum Arguments
* [PR 45](https://github.com/OpenWaterAnalytics/pyswmm/pull/45) - PR: Add release process workflow
* [PR 43](https://github.com/OpenWaterAnalytics/pyswmm/pull/43) - PR: Add code style automatic checks on appveyor
* [PR 41](https://github.com/OpenWaterAnalytics/pyswmm/pull/41) - PR: Clean up code and imports
* [PR 39](https://github.com/OpenWaterAnalytics/pyswmm/pull/39) - PR: Include the output toolkit api
* [PR 38](https://github.com/OpenWaterAnalytics/pyswmm/pull/38) - PR: Clean up code and docs style and clean imports
* [PR 37](https://github.com/OpenWaterAnalytics/pyswmm/pull/37) - Added Link Connection and type helper functions
* [PR 30](https://github.com/OpenWaterAnalytics/pyswmm/pull/30) - Add manifest for pypi packaging
* [PR 29](https://github.com/OpenWaterAnalytics/pyswmm/pull/29) - enhacements to pyswmm.Simulation class
* [PR 28](https://github.com/OpenWaterAnalytics/pyswmm/pull/28) - Add gitattributes, normalize endings
* [PR 24](https://github.com/OpenWaterAnalytics/pyswmm/pull/24) - Add copyright header to files
* [PR 17](https://github.com/OpenWaterAnalytics/pyswmm/pull/17) - Added pyswmm simulation class; restructured and added descriptors
* [PR 3](https://github.com/OpenWaterAnalytics/pyswmm/pull/3) - Enable platform detection and some utilities
* [PR 1](https://github.com/OpenWaterAnalytics/pyswmm/pull/1) - pyswmm house cleaning

In this release 24 pull requests were closed.
