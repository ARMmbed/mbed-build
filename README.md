# Mbed Build

![Package](https://badgen.net/badge/Package/mbed-build/grey)
[![Documentation](https://badgen.net/badge/Documentation/GitHub%20Pages/blue?icon=github)](https://armmbed.github.io/mbed-build)
[![PyPI](https://badgen.net/pypi/v/mbed-build)](https://pypi.org/project/mbed-build/)
[![PyPI - Status](https://img.shields.io/pypi/status/mbed-build)](https://pypi.org/project/mbed-build/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mbed-build)](https://pypi.org/project/mbed-build/)

[![License](https://badgen.net/pypi/license/mbed-build)](https://github.com/ARMmbed/mbed-build/blob/master/LICENSE)
[![Compliance](https://badgen.net/badge/License%20Report/compliant/green?icon=libraries)](https://armmbed.github.io/mbed-build/third_party_IP_report.html)

[![Build Status](https://dev.azure.com/mbed-tools/mbed-build/_apis/build/status/Build%20and%20Release?branchName=master&stageName=CI%20Checkpoint)](https://dev.azure.com/mbed-tools/mbed-build/_build/latest?definitionId=13&branchName=master)
[![Test Coverage](https://codecov.io/gh/ARMmbed/mbed-build/branch/master/graph/badge.svg)](https://codecov.io/gh/ARMmbed/mbed-build)
[![Maintainability](https://api.codeclimate.com/v1/badges/da945b2843e41104c368/maintainability)](https://codeclimate.com/github/ARMmbed/mbed-build/maintainability)

## Overview

**This package provides the core build system for Mbed OS, which relies on [CMake](https://cmake.org/) and [Ninja](https://ninja-build.org/) as underlying technologies.**

The functionality covered in this package includes the following:
- Execution of Mbed Pre-Build stages to determine appropriate configuration for Mbed OS and the build process.
- Invocation of the build process for the command line tools and online build service.
- Export of build instructions to third party command line tools and IDEs.

It is expected that this package will be used by developers of Mbed OS tooling rather than by users of Mbed OS. For
a command line interface for Mbed OS please see the package [mbed-tools](https://github.com/ARMmbed/mbed-tools).

## Releases

For release notes and a history of changes of all **production** releases, please see the following:

- [Changelog](https://github.com/ARMmbed/mbed-build/blob/master/CHANGELOG.md)

For a the list of all available versions please, please see the:

- [PyPI Release History](https://pypi.org/project/mbed-build/#history)

## Versioning

The version scheme used follows [PEP440](https://www.python.org/dev/peps/pep-0440/) and 
[Semantic Versioning](https://semver.org/). For production quality releases the version will look as follows:

- `<major>.<minor>.<patch>`

Beta releases are used to give early access to new functionality, for testing and to get feedback on experimental 
features. As such these releases may not be stable and should not be used for production. Additionally any interfaces
introduced in a beta release may be removed or changed without notice. For **beta** releases the version will look as
follows:

- `<major>.<minor>.<patch>-beta.<pre-release-number>`

## Installation

It is recommended that a virtual environment such as [Pipenv](https://github.com/pypa/pipenv/blob/master/README.md) is
used for all installations to avoid Python dependency conflicts.

To install the most recent production quality release use:

```
pip install mbed-build
```

To install a specific release:

```
pip install mbed-build==<version>
```

## Usage

Interface definition and usage documentation (for developers of Mbed OS tooling) is available for the most recent
production release here:

- [GitHub Pages](https://armmbed.github.io/mbed-build)

## Project Structure

The follow described the major aspects of the project structure:

- `azure-pipelines/` - CI configuration files for Azure Pipelines.
- `docs/` - Interface definition and usage documentation.
- `examples/` - Usage examples.
- `mbed_build/` - Python source files.
- `news/` - Collection of news files for unreleased changes.
- `tests/` - Unit and integration tests.

## Getting Help

- For interface definition and usage documentation, please see [GitHub Pages](https://armmbed.github.io/mbed-build).
- For a list of known issues and possible work arounds, please see [Known Issues](KNOWN_ISSUES.md).
- To raise a defect or enhancement please use [GitHub Issues](https://github.com/ARMmbed/mbed-build/issues).
- To ask a question please use the [Mbed Forum](https://forums.mbed.com/).

## Contributing

- Mbed OS is an open source project and we are committed to fostering a welcoming community, please see our
  [Code of Conduct](https://github.com/ARMmbed/mbed-build/blob/master/CODE_OF_CONDUCT.md) for more information.
- For ways to contribute to the project, please see the [Contributions Guidelines](https://github.com/ARMmbed/mbed-build/blob/master/CONTRIBUTING.md)
- For a technical introduction into developing this package, please see the [Development Guide](https://github.com/ARMmbed/mbed-build/blob/master/DEVELOPMENT.md)
