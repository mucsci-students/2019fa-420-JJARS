# ScrUML
# test_uml_utilities.py
# Team JJARS
from scruml import uml_utilities


def test_parse_class_identifier() -> None:
    assert uml_utilities.parse_class_identifier("Alpha") == "Alpha"

    assert not uml_utilities.parse_class_identifier("")
    assert not uml_utilities.parse_class_identifier("  ")
    assert not uml_utilities.parse_class_identifier("Bad Name")
    assert not uml_utilities.parse_class_identifier("'Bad'Name")
    assert not uml_utilities.parse_class_identifier("[BadName]")


def test_parse_relationship_identifier() -> None:
    assert uml_utilities.parse_relationship_identifier("[Alpha,Beta]")
    assert uml_utilities.parse_relationship_identifier("[Alpha,Beta,relname]")

    assert not uml_utilities.parse_relationship_identifier("[]")
    assert not uml_utilities.parse_relationship_identifier("[Alpha,Beta")
    assert not uml_utilities.parse_relationship_identifier("[Alpha]")
    assert not uml_utilities.parse_relationship_identifier("[Bad Name,Beta]")
    assert not uml_utilities.parse_relationship_identifier("[Alpha,Beta,bad relname]")


def test_classify_identifier() -> None:
    assert uml_utilities.classify_identifier("ClassA") == "class"
    assert uml_utilities.classify_identifier("[ClassA,ClassB]") == "relationship"
    assert (
        uml_utilities.classify_identifier("[ClassA,ClassB,relname]") == "relationship"
    )

    assert not uml_utilities.classify_identifier("b'a'd' n'a'm'e")


def test_stringify_relationship_identifier() -> None:
    assert (
        uml_utilities.stringify_relationship_identifier("Alpha", "Beta")
        == "[Alpha,Beta]"
    )
    assert (
        uml_utilities.stringify_relationship_identifier("Alpha", "Beta", "relname")
        == "[Alpha,Beta,relname]"
    )
