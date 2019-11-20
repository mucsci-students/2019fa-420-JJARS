# ScrUML
# test_uml_utilities.py
# Team JJARS
from scruml import uml_utilities


def test_serialize_variable() -> None:
    assert uml_utilities.serialize_variable("private", "int", "xPos") == (
        "[V:xPos]",
        "[private][int]",
    )
    assert uml_utilities.serialize_variable("", "float", "m_volume") == (
        "[V:m_volume]",
        "[][float]",
    )


def test_serialize_function() -> None:
    assert uml_utilities.serialize_function(
        "public", "string", "getLabel", ["int offset", "char delimiter"]
    ) == ("[F:getLabel]", "[public][string][int][offset][char][delimiter]")
    assert uml_utilities.serialize_function(
        "", "string", "getLabel", ["int offset", "char delimiter"]
    ) == ("[F:getLabel]", "[][string][int][offset][char][delimiter]")
    assert uml_utilities.serialize_function(
        "public", "string", "getLabel", ["int offset"]
    ) == ("[F:getLabel]", "[public][string][int][offset]")
    assert uml_utilities.serialize_function("public", "string", "getLabel", []) == (
        "[F:getLabel]",
        "[public][string]",
    )
    assert uml_utilities.serialize_function("", "string", "getLabel", []) == (
        "[F:getLabel]",
        "[][string]",
    )


def test_deserialize_variable() -> None:
    assert uml_utilities.deserialize_variable("[V:xPos]", "[private][int]") == (
        "private",
        "int",
        "xPos",
    )
    assert uml_utilities.deserialize_variable("[V:m_volume]", "[][float]") == (
        "",
        "float",
        "m_volume",
    )


def test_deserialize_function() -> None:
    assert uml_utilities.deserialize_function(
        "[F:getLabel]", "[public][string][int][offset][char][delimiter]"
    ) == ("public", "string", "getLabel", ["int offset", "char delimiter"])
    assert uml_utilities.deserialize_function(
        "[F:getLabel]", "[][string][int][offset][char][delimiter]"
    ) == ("", "string", "getLabel", ["int offset", "char delimiter"])
    assert uml_utilities.deserialize_function(
        "[F:getLabel]", "[public][string][int][offset]"
    ) == ("public", "string", "getLabel", ["int offset"])
    assert uml_utilities.deserialize_function("[F:getLabel]", "[public][string]") == (
        "public",
        "string",
        "getLabel",
        [],
    )
    assert uml_utilities.deserialize_function("[F:getLabel]", "[][string]") == (
        "",
        "string",
        "getLabel",
        [],
    )


def test_parse_class_identifier() -> None:
    assert uml_utilities.parse_class_identifier("Alpha") == "Alpha"

    assert not uml_utilities.parse_class_identifier("")
    assert not uml_utilities.parse_class_identifier("  ")
    assert not uml_utilities.parse_class_identifier("Bad Name")
    assert not uml_utilities.parse_class_identifier("'Bad'Name")
    assert not uml_utilities.parse_class_identifier("[BadName]")


def test_parse_relationship_identifier() -> None:
    assert uml_utilities.parse_relationship_identifier("[Alpha,Beta]")

    assert not uml_utilities.parse_relationship_identifier("[]")
    assert not uml_utilities.parse_relationship_identifier("[Alpha,Beta")
    assert not uml_utilities.parse_relationship_identifier("[Alpha]")
    assert not uml_utilities.parse_relationship_identifier("[Bad Name,Beta]")
    assert not uml_utilities.parse_relationship_identifier("[Alpha,Beta,bad relname]")


def test_classify_identifier() -> None:
    assert uml_utilities.classify_identifier("ClassA") == "class"
    assert uml_utilities.classify_identifier("[ClassA,ClassB]") == "relationship"

    assert not uml_utilities.classify_identifier("b'a'd' n'a'm'e")


def test_stringify_relationship_identifier() -> None:
    assert (
        uml_utilities.stringify_relationship_identifier("Alpha", "Beta")
        == "[Alpha,Beta]"
    )
