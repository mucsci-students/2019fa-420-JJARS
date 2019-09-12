# ScrUML

### Description

A Simple UML editor written in Python 3.

### Building + Installing

To build and install ScrUML, run:

    pip install .

### Contributing

To get started after a fresh `git clone`, run the following command to install the required packages and set up the git hook scripts:

    pipenv install --dev
    pipenv shell
    pre-commit install

And you're ready to develop! Run `pipenv shell` to activate the virtual environment whenever you begin contributing and `exit` to deactivate the virtual environment whenever you're done.

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
