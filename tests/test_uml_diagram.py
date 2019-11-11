# ScrUML
# test_uml_diagram.py
# Team JJARS
from scruml.uml_diagram import UMLDiagram


def test_add_class() -> None:
    umld: UMLDiagram = UMLDiagram()

    assert umld.add_class("ClassA") == "ClassA"
    assert not umld.add_class("ClassA")
    assert not umld.add_class("ClassA")

    assert umld.add_class("a") == "a"
    assert not umld.add_class("a")

    assert umld.add_class("1234") == "1234"
    assert not umld.add_class("1234")

    assert umld.add_class("None") == "None"
    assert not umld.add_class("None")


def test_remove_class() -> None:
    umld: UMLDiagram = UMLDiagram()

    assert not umld.remove_class("ClassA")
    umld.add_class("ClassA")
    assert umld.remove_class("ClassA") == "ClassA"
    assert not umld.remove_class("ClassA")

    assert not umld.remove_class("a")
    umld.add_class("a")
    assert umld.remove_class("a") == "a"

    assert not umld.remove_class("1234")
    umld.add_class("1234")
    assert umld.remove_class("1234") == "1234"

    assert not umld.remove_class("None")
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

    assert not umld.rename_class("ClassA", "ClassB")
    umld.add_class("ClassA")
    assert umld.rename_class("ClassA", "ClassB") == "ClassB"
    # "ClassA" should no longer exist in the diagram
    assert not umld.rename_class("ClassA", "ClassB")
    assert umld.add_class("ClassA") == "ClassA"
    assert sorted(umld.get_all_class_names()) == ["ClassA", "ClassB"]
    assert not umld.rename_class("ClassA", "ClassB")
    assert not umld.rename_class("ClassB", "ClassA")
    assert not umld.rename_class("NewClass", "ClassB")


def test_set_class_attribute() -> None:
    umld: UMLDiagram = UMLDiagram()

    umld.add_class("ClassA")
    umld.add_class("ClassB")
    # Add valid attributes
    assert umld.set_class_attribute("ClassA", "attr1", "type1") == "type1"
    assert umld.set_class_attribute("ClassA", "attr2", "type2") == "type2"
    assert umld.set_class_attribute("ClassA", "xPos", "int") == "int"
    assert umld.set_class_attribute("ClassB", "attr1", "type1") == "type1"
    # Edit valid attributes
    assert umld.set_class_attribute("ClassA", "attr1", "newType1") == "newType1"
    assert umld.set_class_attribute("ClassA", "attr1", "newType1") == "newType1"
    assert umld.set_class_attribute("ClassA", "attr2", "newType2") == "newType2"
    assert umld.set_class_attribute("ClassA", "xPos", "xPos") == "xPos"
    assert umld.set_class_attribute("ClassB", "attr1", "newType1") == "newType1"
    # Invalid input
    assert not umld.set_class_attribute("fakeClass", "attr1", "val1")


def test_remove_class_attribute() -> None:
    umld: UMLDiagram = UMLDiagram()

    umld.add_class("ClassA")
    umld.add_class("ClassB")
    umld.set_class_attribute("ClassA", "attr1", "type1")
    assert umld.remove_class_attribute("ClassA", "attr1") == "attr1"
    assert not umld.remove_class_attribute("ClassA", "attr1")
    assert not umld.remove_class_attribute("ClassB", "lenth")
    umld.set_class_attribute("ClassB", "length", "size_t")
    assert umld.remove_class_attribute("ClassB", "length") == "length"
    umld.set_class_attribute("ClassB", "name", "string")
    assert not umld.remove_class_attribute("fakeClass", "name")


def test_get_class_attributes() -> None:
    umld: UMLDiagram = UMLDiagram()

    assert not umld.get_class_attributes("fakeClass")
    umld.add_class("ClassA")
    assert not umld.get_class_attributes("ClassA")
    umld.set_class_attribute("ClassA", "name", "string")
    assert umld.get_class_attributes("ClassA") == {"name": "string"}
    umld.set_class_attribute("ClassA", "length", "size_t")
    # Note: dictionary equality comparison does not consider the order of entries
    assert umld.get_class_attributes("ClassA") == {"name": "string", "length": "size_t"}
    umld.set_class_attribute("ClassA", "isValid", "bool")
    assert umld.get_class_attributes("ClassA") == {
        "name": "string",
        "length": "size_t",
        "isValid": "bool",
    }
    umld.remove_class_attribute("ClassA", "length")
    assert umld.get_class_attributes("ClassA") == {"name": "string", "isValid": "bool"}
    umld.remove_class_attribute("ClassA", "name")
    assert umld.get_class_attributes("ClassA") == {"isValid": "bool"}
    umld.remove_class_attribute("ClassA", "isValid")
    assert not umld.get_class_attributes("ClassA")


def test_add_relationship() -> None:
    umld: UMLDiagram = UMLDiagram()
    umld.add_class("Alpha")
    umld.add_class("Beta")
    umld.add_class("Gamma")

    assert umld.add_relationship("Alpha", "Beta")
    assert not umld.add_relationship("Alpha", "Beta")
    assert not umld.add_relationship("Beta", "Alpha")
    assert umld.add_relationship("Alpha", "Beta", "inherits")
    assert not umld.add_relationship("Alpha", "Beta", "inherits")
    assert not umld.add_relationship("Beta", "Alpha", "inherits")
    assert umld.add_relationship("Alpha", "Beta", "produces")
    assert umld.add_relationship("Alpha", "Gamma")
    assert umld.add_relationship("Beta", "Gamma", "inherits")
    assert umld.add_relationship("Gamma", "Gamma")
    assert not umld.add_relationship("Gamma", "Gamma")
    assert umld.add_relationship("Gamma", "Gamma", "observes")
    assert not umld.add_relationship("Gamma", "Gamma", "observes")

    assert not umld.add_relationship("FakeClass", "Alpha")
    assert not umld.add_relationship("Alpha", "FakeClass")
    assert not umld.add_relationship("FakeClass", "FakeClass")


def test_remove_relationship() -> None:
    umld: UMLDiagram = UMLDiagram()
    umld.add_class("Alpha")
    umld.add_class("Beta")
    umld.add_class("Gamma")
    umld.add_relationship("Alpha", "Beta")
    umld.add_relationship("Alpha", "Beta", "inherits")
    umld.add_relationship("Alpha", "Beta", "produces")
    umld.add_relationship("Alpha", "Gamma")
    umld.add_relationship("Gamma", "Gamma")
    umld.add_relationship("Gamma", "Gamma", "observes")

    assert not umld.remove_relationship("Alpha", "Beta", "fake_relation")
    assert umld.remove_relationship("Alpha", "Beta")
    assert not umld.remove_relationship("Alpha", "Beta")
    assert not umld.remove_relationship("Beta", "Alpha")
    assert umld.remove_relationship("Alpha", "Beta", "inherits")
    assert not umld.remove_relationship("Alpha", "Beta", "inherits")
    assert umld.remove_relationship("Alpha", "Beta", "produces")
    assert not umld.remove_relationship("Alpha", "Beta", "produces")
    assert umld.remove_relationship("Alpha", "Gamma")
    assert not umld.remove_relationship("Alpha", "Gamma")
    assert umld.remove_relationship("Gamma", "Gamma")
    assert not umld.remove_relationship("Gamma", "Gamma")
    assert umld.remove_relationship("Gamma", "Gamma", "observes")
    assert not umld.remove_relationship("Gamma", "Gamma", "observes")

    assert not umld.remove_relationship("FakeClass", "Alpha")
    assert not umld.remove_relationship("Alpha", "FakeClass")
    assert not umld.remove_relationship("FakeClass", "FakeClass")


def test_set_relationship_attribute() -> None:
    umld: UMLDiagram = UMLDiagram()
    umld.add_class("Alpha")
    umld.add_class("Beta")
    umld.add_class("Gamma")
    umld.add_relationship("Alpha", "Beta")
    umld.add_relationship("Alpha", "Beta", "inherits")

    assert (
        umld.set_relationship_attribute(
            "Alpha", "Beta", None, "category", "aggregation"
        )
        == "aggregation"
    )
    assert (
        umld.set_relationship_attribute(
            "Alpha", "Beta", "inherits", "quanitfierA", "many"
        )
        == "many"
    )

    assert not umld.set_relationship_attribute(
        "FakeClass", "Beta", "inherits", "category", "aggregation"
    )
    assert not umld.set_relationship_attribute(
        "Alpha", "FakeClass", "inherits", "category", "aggregation"
    )
    assert not umld.set_relationship_attribute(
        "Alpha", "Beta", "FakeRelationshipName", "quanitfierA", "many"
    )
    assert not umld.set_relationship_attribute(
        "Alpha", "Gamma", "inherits", "quanitfierA", "many"
    )


def test_remove_relationship_attribute() -> None:
    umld: UMLDiagram = UMLDiagram()
    umld.add_class("Alpha")
    umld.add_class("Beta")
    umld.add_class("Gamma")
    umld.add_relationship("Alpha", "Beta")
    umld.add_relationship("Alpha", "Beta", "inherits")

    umld.set_relationship_attribute("Alpha", "Beta", None, "category", "aggregation")
    umld.set_relationship_attribute("Alpha", "Beta", "inherits", "quanitfierA", "many")

    assert (
        umld.remove_relationship_attribute("Alpha", "Beta", None, "category")
        == "category"
    )
    assert not umld.remove_relationship_attribute("Alpha", "Beta", None, "category")

    assert (
        umld.remove_relationship_attribute("Alpha", "Beta", "inherits", "quanitfierA")
        == "quanitfierA"
    )
    assert not umld.remove_relationship_attribute(
        "Alpha", "Beta", "inherits", "quanitfierA"
    )

    assert not umld.remove_relationship_attribute(
        "FakeClass", "Beta", "inherits", "category"
    )
    assert not umld.remove_relationship_attribute(
        "Alpha", "FakeClass", "inherits", "category"
    )
    assert not umld.remove_relationship_attribute(
        "Alpha", "Beta", "FakeRelationshipName", "quanitfierA"
    )
    assert not umld.remove_relationship_attribute(
        "Alpha", "Beta", "inherits", "FakeRelAttrName"
    )
    assert not umld.remove_relationship_attribute(
        "Alpha", "Gamma", "inherits", "quanitfierA"
    )


def test_get_relationship_attributes() -> None:
    umld: UMLDiagram = UMLDiagram()
    umld.add_class("Alpha")
    umld.add_class("Beta")
    umld.add_class("Gamma")
    umld.add_relationship("Alpha", "Beta")
    umld.add_relationship("Alpha", "Beta", "inherits")

    assert not umld.get_relationship_attributes("Alpha", "Beta")
    assert not umld.get_relationship_attributes("Alpha", "Beta", "inherits")

    umld.set_relationship_attribute("Alpha", "Beta", None, "category", "aggregation")
    assert umld.get_relationship_attributes("Alpha", "Beta") == {
        "category": "aggregation"
    }

    umld.remove_relationship_attribute("Alpha", "Beta", None, "category")
    assert not umld.get_relationship_attributes("Alpha", "Beta")

    umld.set_relationship_attribute("Alpha", "Beta", "inherits", "quanitfierA", "many")
    assert umld.get_relationship_attributes("Alpha", "Beta", "inherits") == {
        "quanitfierA": "many"
    }
    umld.set_relationship_attribute("Alpha", "Beta", "inherits", "quanitfierB", "one")
    assert umld.get_relationship_attributes("Alpha", "Beta", "inherits") == {
        "quanitfierA": "many",
        "quanitfierB": "one",
    }
    umld.set_relationship_attribute(
        "Alpha", "Beta", "inherits", "category", "generalization"
    )
    assert umld.get_relationship_attributes("Alpha", "Beta", "inherits") == {
        "quanitfierA": "many",
        "quanitfierB": "one",
        "category": "generalization",
    }

    umld.remove_relationship_attribute("Alpha", "Beta", "inherits", "quanitfierB")
    assert umld.get_relationship_attributes("Alpha", "Beta", "inherits") == {
        "quanitfierA": "many",
        "category": "generalization",
    }
    umld.remove_relationship_attribute("Alpha", "Beta", "inherits", "quanitfierA")
    assert umld.get_relationship_attributes("Alpha", "Beta", "inherits") == {
        "category": "generalization"
    }
    umld.remove_relationship_attribute("Alpha", "Beta", "inherits", "category")
    assert not umld.get_relationship_attributes("Alpha", "Beta", "inherits")

    assert not umld.get_relationship_attributes("FakeClass", "Beta")
    assert not umld.get_relationship_attributes("Alpha", "FakeClass")
    assert not umld.get_relationship_attributes("Alpha", "Beta", "FakeRelationshipName")
    assert not umld.get_relationship_attributes("Alpha", "Gamma")
