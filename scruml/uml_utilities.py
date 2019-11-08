# ScrUML
# uml_utilities.py
# Team JJARS
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


# ----------
# parse_class_identifier


def parse_class_identifier(ident: str) -> Optional[str]:
    """Returns valid class identifier on success, or None on failure.
Valid class identifiers contain no whitespace, no quotes, and are not surrounded by brackets."""

    ident = ident.strip()
    if " " in ident:
        return None
    if '"' in ident:
        return None
    if "'" in ident:
        return None
    if ident.startswith("[") and ident.endswith("]"):
        return None
    return ident


# ----------
# parse_relationship_identifier


def parse_relationship_identifier(
    ident: str
) -> Optional[Tuple[str, str, Optional[str]]]:
    """Returns valid relationship identifier on success, or None on failure.
Valid relationship identifiers are surrounded by brackets, contain two valid class names
separated by a comma, and an optional relationship name (also comma separated)."""

    ident = ident.strip()

    # Check for start and end brackets and then shear them away
    if ident.startswith("[") and ident.endswith("]"):
        ident = ident[1:-1]
    else:
        return None

    # Split up the string into a list
    ident_list: List[str] = ident.split(",")

    # Make sure that there were enough values provided in the identifier
    if len(ident_list) <= 1 or len(ident_list) >= 4:
        return None

    # Pull out and validate the two class names that should be in the identifier
    class_A_name: Optional[str] = parse_class_identifier(ident_list[0])
    class_B_name: Optional[str] = parse_class_identifier(ident_list[1])
    if not class_A_name or not class_B_name:
        return None

    # If a relationship name was provided, pull it out and validate it too
    # (Relationship names follow the same rules as class names for simplicity)
    relationship_name: Optional[str] = None
    if len(ident_list) == 3:
        relationship_name = parse_class_identifier(ident_list[2])
        if not relationship_name:
            return None

    return (str(class_A_name), str(class_B_name), relationship_name)


# ----------
# classify_identifier


def classify_identifier(ident: str) -> Optional[str]:
    """Returns a string identifying the kind of identifier that "ident" represents.
Possible values: "class", "relationship", None"""

    if parse_class_identifier(ident):
        return "class"
    elif parse_relationship_identifier(ident):
        return "relationship"
    else:
        return None


# ----------
# stringify_relationship_identifier


def stringify_relationship_identifier(
    class_name_a: str, class_name_b: str, relationship_name: Optional[str] = None
) -> str:
    """Returns a stringified relationship identifier from the provided class names and (optional) relationship name."""

    return "[{},{}{}]".format(
        class_name_a,
        class_name_b,
        "" if not relationship_name else "," + relationship_name,
    )
