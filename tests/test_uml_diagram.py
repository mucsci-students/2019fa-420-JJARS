# ScrUML
# test_uml_diagram.py
# Team JJARS
from scruml.uml_diagram import UMLDiagram


def test_add_class() -> None:
    umld: UMLDiagram = UMLDiagram()

    assert umld.add_class("ClassA") == "ClassA"
    assert umld.add_class("ClassA") == None
    assert umld.add_class("ClassA") == None

    assert umld.add_class("a") == "a"
    assert umld.add_class("a") == None

    assert umld.add_class("1234") == "1234"
    assert umld.add_class("1234") == None

    assert umld.add_class("None") == "None"
    assert umld.add_class("None") == None


def test_remove_class() -> None:
    umld: UMLDiagram = UMLDiagram()

    assert umld.remove_class("ClassA") == None
    umld.add_class("ClassA")
    assert umld.remove_class("ClassA") == "ClassA"
    assert umld.remove_class("ClassA") == None

    assert umld.remove_class("a") == None
    umld.add_class("a")
    assert umld.remove_class("a") == "a"

    assert umld.remove_class("1234") == None
    umld.add_class("1234")
    assert umld.remove_class("1234") == "1234"

    assert umld.remove_class("None") == None
    umld.add_class("None")
    assert umld.remove_class("None") == "None"


def test_get_all_class_names() -> None:
    umld: UMLDiagram = UMLDiagram()

    assert umld.get_all_class_names() == []
    umld.add_class("ClassA")
    assert umld.get_all_class_names() == ["ClassA"]
    umld.add_class("a")
    # order not guaranteed, sort for the comparison
    assert sorted(umld.get_all_class_names()) == ["ClassA", "a"]
    umld.add_class("1234")
    assert sorted(umld.get_all_class_names()) == ["1234", "ClassA", "a"]
    umld.remove_class("ClassA")
    assert sorted(umld.get_all_class_names()) == ["1234", "a"]
    umld.remove_class("1234")
    assert umld.get_all_class_names() == ["a"]
    umld.remove_class("a")
    assert umld.get_all_class_names() == []


def test_rename_class() -> None:
    umld: UMLDiagram = UMLDiagram()

    assert umld.rename_class("ClassA", "ClassB") == None
    umld.add_class("ClassA")
    assert umld.rename_class("ClassA", "ClassB") == "ClassB"
    # "ClassA" should no longer exist in the diagram
    assert umld.rename_class("ClassA", "ClassB") == None
    assert umld.add_class("ClassA") == "ClassA"
    assert sorted(umld.get_all_class_names()) == ["ClassA", "ClassB"]
    assert umld.rename_class("ClassA", "ClassB") == None
    assert umld.rename_class("ClassB", "ClassA") == None
    assert umld.rename_class("NewClass", "ClassB") == None
