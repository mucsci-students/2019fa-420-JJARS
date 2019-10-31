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
    assert result == ""

    result2 = api.addClass({"x": 0, "y": 20, "class_name": "classA"})
    assert result2 == "Class classA already exists in the diagram."

    result3 = api.addClass({"x": 0, "y": 20, "class_name": "class A"})
    assert (
        result3
        == "Class name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"
    )

    result4 = api.addClass({"x": 20, "y": 20, "class_name": "classB"})
    assert result4 == ""

    resultA = api.removeClass("class_name": "class1")
    assert resultA == "Selected class not found in diagram: class1"

    resultB = api.addClass({"x": 0, "y": 20, "class_name": "class1"})
    assert resultB == ""
    
    resultC = api.removeClass("class_name": "class1")
    assert resultC == ""
    # assert api.__diagram.add_class("classA")
    # assert api.__diagram.add_class("classB")

    # result5 = api.removeClass({'class_name': "classA"})
    # return result5 == ""


# assert api.__diagram.get_all_class_names() == []


def test_set_class_attribute() -> str:
    api: __API = __API()

    # result = api.setClassAttribute({"class_name": "classA", "attribute_name": "Foo Bar", "attribute_value": 20})
    # return result == "Attribute name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"

    result2 = api.setClassAttribute(
        {"class_name": "classA", "attribute_name": "Foo Bar", "attribute_value": "20"}
    )
    att_name = result2.get("attribute_name", "Foo Bar")
    assert (
        result2
        == "Class"
        + {"class_name"}
        + "does not exist in the diagram. Unable to add attribute:"
        + att_name
    )
def test_remove_class_attribute() -> str:
    api: __API = __API()

    result1 = api.addClass({"x": 0, "y":20, "class_name": "class1"})
    assert result1 == ""

    result2 = api.setClassAttribute({"class_name": "class1", "attribute_name": "foo", "attribute_value": "20"})
    assert result2 == ""

    result3 = api.removeClassAttribute("class_name": "class1", "attribute_name": "bar")
    assert result3 == "Attribute " + attribute_name + " not found in Class: " + class_name

    result4 = api.removeClassAttribute("class_name": "class1", "attribute_name": "foo")
    assert result4 == ""
