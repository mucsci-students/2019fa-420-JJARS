# ScrUML [![Build Status](https://travis-ci.org/mucs420f19/JJARS.svg?branch=develop)](https://travis-ci.org/mucs420f19/JJARS) [![Coverage Status](https://coveralls.io/repos/github/mucs420f19/JJARS/badge.svg?branch=develop)](https://coveralls.io/github/mucs420f19/JJARS?branch=develop)

Version 1.0.0

### Description

A Simple UML editor written in Python 3 using [pywebview](https://github.com/r0x0r/pywebview).

### Requirements

A functioning Python >3.6 installation is required to run ScrUML.

PIP is required for the installation process.

### Building + Installing

To build and install ScrUML, run:

    pip install .

### Running

To open ScrUML after installation, just run:

    scruml

If you want to use the command line interface:

    scruml --cli

### Contributing

To get started after a fresh `git clone`, run the following command to install the required packages and set up the git hook scripts:

    pipenv install --dev
    pipenv shell
    pre-commit install

And you're ready to develop! Run `pipenv shell` to activate the virtual environment whenever you begin contributing and `exit` to deactivate the virtual environment whenever you're done.

You may want to build ScrUML with `pip install -e .` to install the package in editable mode, which will allow for any changes to affect the program without having to reinstall it.

### Tests

Testing is performed with `pytest` using the following test layout:

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
