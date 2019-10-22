#!/bin/bash

# Generates project documentation using pdoc
pdoc --html --force -c show_type_annotations=True -o docs/ scruml
