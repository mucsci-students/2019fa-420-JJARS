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
    assert not result2 == ""

    add_class_data_case_2 = {"class_name": "class A", "x": 0, "y": 20}

    result3 = api.addClass(add_class_data_case_2)
    assert not result3 == ""

    try:
        api.removeClass(add_class_data["class_name"])
        assert False
    except Exception as e:
        assert True


def test_set_and_remove_class_attribute() -> str:
    api: __API = __API()
    api._API__diagram = UMLDiagram()

    # Test setClassAttribute
    # Failure cases
    test_data = {
        "class_name": "classA",
        "attribute_category": "metadata",
        "attribute_name": "Foo Bar",
        "attribute_value": "20",
    }
    result = api.setClassAttribute(test_data)
    assert not result == ""

    set_att_data = {
        "class_name": "classA",
        "attribute_category": "metadata",
        "attribute_name": "Foo_Bar",
        "attribute_value": "20",
        "ignore_naming_rules": "t",
    }
    result2 = api.setClassAttribute(set_att_data)
    assert not result2 == ""

    # Successful cases
    add_class_data = {"class_name": "classA", "x": 0, "y": 20}
    result3 = api.addClass(add_class_data)
    correct_metadata_data = {
        "class_name": "classA",
        "attribute_category": "metadata",
        "attribute_name": "Foo_Bar",
        "attribute_value": "20",
        "ignore_naming_rules": "t",
    }
    result4 = api.setClassAttribute(correct_metadata_data)
    assert result4 == ""

    correct_func_params_data = {
        "class_name": "classA",
        "attribute_category": "function",
        "func_visibility": "private",
        "func_return_type": "int",
        "func_name": "myFunc",
        "func_params": "int x, float y",
    }
    result5 = api.setClassAttribute(correct_func_params_data)
    assert result5 == ""

    correct_func_no_params_data = {
        "class_name": "classA",
        "attribute_category": "function",
        "func_visibility": "private",
        "func_return_type": "int",
        "func_name": "myOtherFunc",
        "func_params": "",
    }
    result6 = api.setClassAttribute(correct_func_no_params_data)
    assert result6 == ""

    correct_variable_data = {
        "class_name": "classA",
        "attribute_category": "variable",
        "var_visibility": "public",
        "var_type": "string",
        "var_name": "myName",
    }
    result7 = api.setClassAttribute(correct_variable_data)
    assert result7 == ""

    # Test removeClassAttribute
    # Failure case
    bad_attr_data = {"class_name": "classA", "attribute_name": "fakeAttr"}
    result8 = api.removeClassAttribute(bad_attr_data)
    assert not result8 == ""

    # Successful case
    good_attr_data = {"class_name": "classA", "attribute_name": "[V:myName]"}
    result9 = api.removeClassAttribute(good_attr_data)
    assert result9 == ""


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
    assert not result == ""
    result = api.addRelationship(
        {"class_name_a": "classC", "class_name_b": "classB", "relationship_name": ""}
    )
    assert not result == ""

    result = api.removeRelationship("[classA,classB]")
    assert result == ""
    result = api.removeRelationship("[classA,classB]")
    assert not result == ""
    result = api.removeRelationship("[classC,classB]")
    assert not result == ""
    result = api.removeRelationship("[classA,classC]")
    assert not result == ""


def test_rename_class() -> None:
    api: __API = __API()

    add_class_data = {"class_name": "classA", "x": 0, "y": 20}
    result = api.addClass(add_class_data)
    rename_class_data1 = {"old_class_name": "classA", "new_class_name": "thisNewClass"}
    result1 = api.renameClass(rename_class_data1)
    assert result1 == ""

    rename_class_data2 = {"old_class_name": "old class", "new_class_name": "newClass"}
    result2 = api.renameClass(rename_class_data2)
    assert not result2 == ""

    rename_class_data3 = {"old_class_name": "oldClass", "new_class_name": "new class"}
    result3 = api.renameClass(rename_class_data3)
    assert not result3 == ""

    rename_class_data4 = {"old_class_name": "oldClass", "new_class_name": "newClass"}
    result4 = api.renameClass(rename_class_data4)
    assert not result4 == ""
