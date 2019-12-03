
# ScrUML [![Build Status](https://travis-ci.org/mucs420f19/JJARS.svg?branch=develop)](https://travis-ci.org/mucs420f19/JJARS) [![Coverage Status](https://coveralls.io/repos/github/mucs420f19/JJARS/badge.svg?branch=develop)](https://coveralls.io/github/mucs420f19/JJARS?branch=develop)

![Screenshot](/assets/screenshot.png?raw=true)

Version 4.0.0

## Table of Contents

- [Description](#description)
- [Requirements](#requirements)
- [Building + Installing](#building--installing)
- [Running](#running)
- [Contributing](#contributing)
- [Known Issues](#known-issues)
  - [Windows](#windows)
  - [Linux](#linux)
  - [MacOS](#macos)
- [Documentation](#documentation)
- [Testing](#testing)

## Description

A Simple UML editor written in Python 3 using [pywebview](https://github.com/r0x0r/pywebview).

Compatible with Windows 10 and Linux. (MacOS support is a [work in progress.](#macos))

## Requirements

A functioning Python >3.6 installation is required to run ScrUML.

PIP is required for the installation process.

## Building + Installing

To build and install ScrUML, run:

    pip install .

## Running

To open ScrUML after installation, just run:

    scruml

If you want to use the command line interface:

    scruml --cli

## Contributing

To get started after a fresh `git clone`, run the following command to install the required packages and set up the git hook scripts:

    pipenv install --dev
    pipenv shell
    pre-commit install

And you're ready to develop! Run `pipenv shell` to activate the virtual environment whenever you begin contributing and `exit` to deactivate the virtual environment whenever you're done.

You may want to build ScrUML with `pip install -e .` to install the package in editable mode, which will allow for any changes to affect the program without having to reinstall it.


## Known Issues

### Windows

- None

### Linux

- None

### MacOS

- [Keyboard focus is broken when running in a virtual environment](https://github.com/r0x0r/pywebview/issues/66)
- [Drag events are not reported properly by the webview](https://github.com/mucs420f19/JJARS/issues/141)

## Documentation

Documentation is automatically generated from docstrings with `pdoc`.

To update the documentation, run the `pdoc.sh` file in the root of the repository.

## Testing

Testing is performed with `pytest` using the following file layout:

    setup.py
    scruml/
        __init__.py
        example.py
        subfolder/
            another_example.py
    tests/
        test_example.py
        subfolder/
            test_another_example.py
        ...

Static type analysis and automatic formatting are provided by `mypy` and `black`.
