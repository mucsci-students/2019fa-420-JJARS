# ScrUML
# test_uml_context_cli.py
# Team JJARS
# type: ignore
from pathlib import Path
from typing import List

import pytest

import scruml.uml_context_cli
from scruml.uml_context_cli import __UMLShell
from scruml.uml_diagram import UMLDiagram


def test_add_and_remove_classes() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("add classA")
    shell.onecmd("add classB")
    shell.onecmd("add [invalidclass]")
    shell.onecmd("add invalid class")
    shell.onecmd("add 'invalidclass'")
    shell.onecmd('add "invalidclass"')
    shell.onecmd("add [classA,classB]")
    shell.onecmd("add [classA,classB,myname]")
    shell.onecmd("add [[invalidrelationship],invalid class]")
    shell.onecmd("add [invalid class,[invalidrelationship],somename]")

    assert not shell._UMLShell__diagram.add_class("classA")
    assert not shell._UMLShell__diagram.add_class("classB")
    assert sorted(shell._UMLShell__diagram.get_all_class_names()) == [
        "classA",
        "classB",
    ]

    shell.onecmd("remove classA")
    shell.onecmd("remove classB")
    shell.onecmd("remove [invalidclass]")
    shell.onecmd("remove invalid class")
    shell.onecmd("remove [classA,classB]")
    shell.onecmd("remove [classA,classB,myname]")
    shell.onecmd("remove [[invalidrelationship],invalid class]")
    shell.onecmd("remove [invalid class,[invalidrelationship],somename]")
    shell.onecmd("remove [classA,classB,bad name]")

    assert shell._UMLShell__diagram.get_all_class_names() == []


def test_rename() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("add classA")
    shell.onecmd("add classA")
    shell.onecmd("add classB")
    shell.onecmd("rename classA classC")

    assert sorted(shell._UMLShell__diagram.get_all_class_names()) == [
        "classB",
        "classC",
    ]

    shell.onecmd("rename classB")

    assert sorted(shell._UMLShell__diagram.get_all_class_names()) == [
        "classB",
        "classC",
    ]

    shell.onecmd("remove classB")
    shell.onecmd("remove classC")
    shell.onecmd("remove classC")
    shell.onecmd("add classA")
    shell.onecmd("rename classA [classB]")
    shell.onecmd("rename classZOINKS classB")
    shell.onecmd("rename classA classA")

    assert shell._UMLShell__diagram.get_all_class_names() == ["classA"]

    # TODO: Update this when renaming is fully implemented, should probably be removed
    shell._UMLShell__rename_class("Not implemented")
    shell._UMLShell__rename_relationship("Not implemented")


def test_add_and_remove_relationships() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("add classA")
    shell.onecmd("add classB")

    assert shell._UMLShell__diagram.get_all_relationship_pairs() == []

    shell.onecmd("add [classC,classB]")
    shell.onecmd("add [classA,classC]")

    assert shell._UMLShell__diagram.get_all_relationship_pairs() == []

    shell.onecmd("add [classA,classB]")
    shell.onecmd("add [classA,classB]")
    shell.onecmd("add [classA,classB,inherits]")
    shell.onecmd("add [classB,classA,extends]")

    assert shell._UMLShell__diagram.get_all_relationship_pairs() == [
        ("classA", "classB")
    ]

    shell.onecmd("remove [classC,classB]")
    shell.onecmd("remove [classA,classC]")
    shell.onecmd("remove [classA,classB,doesntexist]")

    assert shell._UMLShell__diagram.get_all_relationship_pairs() == [
        ("classA", "classB")
    ]

    shell.onecmd("remove [classA,classB]")
    shell.onecmd("remove [classA,classB,inherits]")

    assert shell._UMLShell__diagram.get_all_relationship_pairs() == [
        ("classA", "classB")
    ]

    shell.onecmd("remove [classA,classB,extends]")

    assert shell._UMLShell__diagram.get_all_relationship_pairs() == []

    shell.onecmd("add [classA,fakeClass]")
    shell.onecmd("remove [fakeClass,classB]")

    assert shell._UMLShell__diagram.get_all_relationship_pairs() == []


def test_set_and_strip_class_attributes() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("add classA")

    shell.onecmd("set classA length size_t")
    shell.onecmd("set classA isValid bool")
    shell.onecmd("set classA")
    shell.onecmd("set classA a")
    shell.onecmd("set classA a b c d")
    shell.onecmd("set classA 'badname' value")

    assert shell._UMLShell__diagram.get_class_attributes("classA") == {
        "length": "size_t",
        "isValid": "bool",
    }

    shell.onecmd("strip classA length")
    shell.onecmd("strip classA isValid")
    shell.onecmd("strip classA")
    shell.onecmd("strip classA a")
    shell.onecmd("strip classA a b c d")
    shell.onecmd("strip classA 'badname'")

    assert shell._UMLShell__diagram.get_class_attributes("classA") == {}

    shell.onecmd("strip classA fakeAttr")
    shell.onecmd("set fakeClass length size_t")
    shell.onecmd("strip fakeClass fakeAttr")

def test_set_and_strip_relationship_attribute() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("add class1")
    shell.onecmd("add class2")
    shell.onecmd("add class3")
    shell.onecmd("add [class1,class2,fakeName]")
    shell.onecmd("add [class2,class3]")
    shell.onecmd("set [class1,class2,fakeName] category aggregate")
    shell.onecmd("set [class2,class3] category aggregate")

    assert shell._UMLShell__diagram.get_relationship_attributes("class1", "class2", "fakeName") == {"category": "aggregate"}
    assert shell._UMLShell__diagram.get_relationship_attributes("class2","class3",None) == {"category": "aggregate"}

    shell.onecmd("strip [class2,class3] category")
    shell.onecmd("strip [class1,class2,fakeName] category")

    assert shell._UMLShell__diagram.get_relationship_attributes("class2","class3",None) == {}
    assert shell._UMLShell__diagram.get_relationship_attributes("class1", "class2", "fakeName") == {}

def test_rename() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("add classA")
    shell.onecmd("add classA")
    shell.onecmd("add classB")
    shell.onecmd("rename classA classC")

    assert sorted(shell._UMLShell__diagram.get_all_class_names()) == [
        "classB",
        "classC",
    ]

    shell.onecmd("rename classB")

    assert sorted(shell._UMLShell__diagram.get_all_class_names()) == [
        "classB",
        "classC",
    ]

    shell.onecmd("remove classB")
    shell.onecmd("remove classC")
    shell.onecmd("remove classC")
    shell.onecmd("add classA")
    shell.onecmd("rename classA [classB]")
    shell.onecmd("rename classZOINKS classB")
    shell.onecmd("rename classA classA")

    assert shell._UMLShell__diagram.get_all_class_names() == ["classA"]

    # TODO: Update this when renaming is fully implemented, should probably be removed
    shell._UMLShell__rename_class("Not implemented")
    shell._UMLShell__rename_relationship("Not implemented")


def test_complete() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("add lcassC")
    shell.onecmd("add abc")
    shell.onecmd("add classA")
    shell.onecmd("add classB")
    shell.onecmd("add class12")

    assert shell.complete_remove("clas", "remove clas", 7, 11) == [
        "classA",
        "classB",
        "class12",
    ]
    assert shell.complete_remove("lcas", "remove clas", 7, 11) == ["lcassC"]
    assert shell.complete_remove("nart", "remove clas", 7, 11) == []

    assert shell.complete_rename("clas", "rename clas", 7, 11) == [
        "classA",
        "classB",
        "class12",
    ]
    assert shell.complete_rename("lcas", "rename clas", 7, 11) == ["lcassC"]
    assert shell.complete_rename("nart", "rename clas", 7, 11) == []


def test_save_and_load(tmp_path: Path):
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()
    file_path: str = str(tmp_path / "saveandloadtest.yaml")

    shell.onecmd("save")
    shell.onecmd(
        "save '\\乃工厶 匚卄凵𠘨厶凵丂!//#$!(*"
        "*)'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
    shell.onecmd("load")
    shell.onecmd(
        "load '\\乃工厶 匚卄凵𠘨厶凵丂!//#$!(*"
        "*)'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )

    shell.onecmd("add classToLoad")
    assert shell._UMLShell__diagram.get_all_class_names() == ["classToLoad"]

    shell.onecmd("save " + file_path)

    scruml.uml_context_cli.input = lambda s: "n"
    shell.onecmd("load " + file_path)

    shell.onecmd("remove classToLoad")
    assert shell._UMLShell__diagram.get_all_class_names() == []

    shell.onecmd("load " + file_path)
    assert shell._UMLShell__diagram.get_all_class_names() == ["classToLoad"]


def test_print() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("print")
    shell.onecmd("add classA")
    shell.onecmd("add classB")
    shell.onecmd("print")
    shell.onecmd("add [classA,classB]")
    shell.onecmd("print")


def test_yes_no_prompt() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    scruml.uml_context_cli.input = lambda s: "y"
    shell._UMLShell__yes_or_no_prompt("Test prompt 1")
    scruml.uml_context_cli.input = lambda s: "n"
    shell._UMLShell__yes_or_no_prompt("Test prompt 2")


def test_exit() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    scruml.uml_context_cli.input = lambda s: "n"
    shell.onecmd("exit")
    scruml.uml_context_cli.input = lambda s: "y"
    shell.onecmd("exit")


def test_help() -> None:
    shell: __UMLShell = __UMLShell()
    shell._UMLShell__diagram = UMLDiagram()

    shell.onecmd("")
    shell.onecmd("help")
    shell.onecmd("help identifiers")
