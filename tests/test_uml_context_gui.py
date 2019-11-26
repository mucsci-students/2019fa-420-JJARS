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

    add_class_data = {"class_name": "classA", "x": 0, "y": 20}

    result = api.addClass(add_class_data)
    assert result == ""

    result2 = api.addClass(add_class_data)
    assert result2 == "Class classA already exists in the diagram."

    add_class_data_case_2 = {"class_name": "class A", "x": 0, "y": 20}

    result3 = api.addClass(add_class_data_case_2)
    assert (
        result3
        == "Class name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"
    )

    try:
        api.removeClass(add_class_data["class_name"])
        assert False
        # print(f"Selected class not found in diagram. Unable to add attribute: {add_class_data['class_name']}")
    except Exception as e:
        assert True
        # print(f"Selected class not found in diagram. Unable to add attribute: {add_class_data['class_name']}")


def test_set_and_remove_class_attribute() -> str:
    api: __API = __API()
    api._API__diagram = UMLDiagram()

    test_data = {
        "class_name": "classA",
        "attribute_name": "Foo Bar",
        "attribute_value": "20",
    }
    result = api.setClassAttribute(test_data)
    assert (
        result
        == "Attribute name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"
    )

    set_att_data = {
        "class_name": "classA",
        "attribute_name": "Foo_Bar",
        "attribute_value": "20",
        "ignore_naming_rules": "t",
    }
    result2 = api.setClassAttribute(set_att_data)
    assert (
        result2
        == f"Class {set_att_data['class_name']} does not exist in the diagram. Unable to add attribute: {set_att_data['attribute_name']}"
    )

    result3 = api.removeClassAttribute(
        set_att_data["class_name"], set_att_data["attribute_name"]
    )
    assert (
        result3
        == f"Attribute {set_att_data['attribute_name']} not found in Class: {set_att_data['class_name']}"
    )

    add_class_data = {"class_name": "classA", "x": 0, "y": 20}
    result4 = api.addClass(add_class_data)
    correct_att_data = {
        "class_name": "classA",
        "attribute_name": "Foo_Bar",
        "attribute_value": "20",
        "ignore_naming_rules": "t",
    }
    result5 = api.setClassAttribute(correct_att_data)
    assert result5 == ""


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
    assert result == "Relationship not found in diagram: [classA,classB]"
    result = api.removeRelationship("[classC,classB]")
    assert result == "Class classC not found in the diagram."
    result = api.removeRelationship("[classA,classC]")
    assert result == "Class classC not found in the diagram."


def test_rename_class() -> None:
    api: __API = __API()

    add_class_data = {"class_name": "classA", "x": 0, "y": 20}
    result = api.addClass(add_class_data)
    rename_class_data1 = {"old_class_name": "classA", "new_class_name": "thisNewClass"}
    result1 = api.renameClass(rename_class_data1)
    assert result1 == ""

    rename_class_data2 = {"old_class_name": "old class", "new_class_name": "newClass"}
    result2 = api.renameClass(rename_class_data2)
    assert (
        result2
        == "Old class name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"
    )

    rename_class_data3 = {"old_class_name": "oldClass", "new_class_name": "new class"}
    result3 = api.renameClass(rename_class_data3)
    assert (
        result3
        == "New class name is invalid. (Cannot contain whitespace or quotes, and cannot be surrounded by brackets.)"
    )

    rename_class_data4 = {"old_class_name": "oldClass", "new_class_name": "newClass"}
    result4 = api.renameClass(rename_class_data4)
    assert (
        result4
        == f"Class {rename_class_data2['new_class_name']} already exists in the diagram."
    )
