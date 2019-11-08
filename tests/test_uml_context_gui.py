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
    api._API__diagram = UMLDiagram()

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

    # assert api.__diagram.add_class("classA")
    # assert api.__diagram.add_class("classB")

    # result5 = api.removeClass({'class_name': "classA"})
    # return result5 == ""


# assert api.__diagram.get_all_class_names() == []


def test_set_class_attribute() -> str:
    api: __API = __API()
    api._API__diagram = UMLDiagram()
    """
    test_data = {
        "class_name": "classA",
        "attribute_name": "Foo Bar",
        "attribute_value": "20",
        "ignore_naming_rules": "t",
    }
    result = api.setClassAttribute(test_data)
    assert (
     	result
     	== "Attribute name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"
    )
    """

    data = {
        "class_name": "classA",
        "attribute_name": "Foo Bar",
        "attribute_value": "20",
        "ignore_naming_rules": "t",
    }
    result2 = api.setClassAttribute(data)
    assert (
        result2
        == f"Class {data['class_name']} does not exist in the diagram. Unable to add attribute: {data['attribute_name']}"
    )


def test_add_and_remove_relationship() -> None:
    api: __API = __API()

    api.addClass({"x": 0, "y": 20, "class_name": "classA"})
    api.addClass({"x": 20, "y": 20, "class_name": "classB"})
    result = api.addRelationship(
        {"class_name_a": "classA", "class_name_b": "classB", "relationship_name": ""}
    )
    assert result == ""
    result = api.addRelationship(
        {"class_name_a": "classA", "class_name_b": "classB", "relationship_name": ""}
    )
    assert result == "Relationship already exists: [classA,classB]"
    result = api.addRelationship(
        {"class_name_a": "classC", "class_name_b": "classB", "relationship_name": ""}
    )
    assert result == "Class classC not found in the diagram."

    result = api.removeRelationship("[classA,classB]")
    assert result == ""
    result = api.removeRelationship("[classA,classB]")
    assert result == "Relationship not found in diagram: [ classA,classB]"
    result = api.removeRelationship("[classC,classB]")
    assert result == "Class classC not found in the diagram."
    result = api.removeRelationship("[classA,classC]")
    assert result == "Class classC not found in the diagram."
