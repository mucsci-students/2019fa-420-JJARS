# ScrUML
# test_uml_context_gui.py
# Team JJARS
# type: ignore
from pathlib import Path
from typing import List

import pytest

import scruml.uml_context_gui
from scruml.uml_context_gui import __API
from scruml.uml_diagram import UMLDiagram


def test_activate() -> None:
    # TODO: To be updated with the context_gui module
    # scruml.uml_context_gui.activate()
    pass


def test_add_and_remove_class() -> None:
    api: __API = __API()
    # api.__diagram = UMLDiagram()

    result = api.addClass({"x": 0, "y": 20, "class_name": "classA"})
    return result == ""

    result2 = api.addClass({"x": 0, "y": 20, "class_name": "classA"})
    return result2 == "Class classA already exist"

    result3 = api.addClass({"x": 0, "y": 20, "class_name": "class A"})
    return (
        result3
        == "Class name is invalid, contains whitespace or is surrounded by brackets"
    )

    result4 = api.addClass({"x": 20, "y": 20, "class_name": "classB"})
    return result4 == ""

    # assert api.__diagram.add_class("classA")
    # assert api.__diagram.add_class("classB")

    # result5 = api.removeClass({'class_name': "classA"})
    # return result5 == ""


# assert api.__diagram.get_all_class_names() == []
