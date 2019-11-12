# ScrUML
# uml_utilities.py
# Team JJARS
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple


# ----------
# serialize_variable


def serialize_variable(
    var_visibility: str, var_type: str, var_name: str
) -> Tuple[str, str]:
    """Returns a tuple of strings (class_attr_key, class_attr_value) where
class_attr_key is in the form: "[V:var_name]" and
class_attr_value is in the form "[var_visibility][var_type]".
If no visibility was specified (var_visibility==""), then class_attr_value is "[][var_type]"."""

    var_visibility = var_visibility.strip()
    var_type = var_type.strip()
    var_name = var_name.strip()

    return (f"[V:{var_name}]", f"[{var_visibility}][{var_type}]")


# ----------
# serialize_function


def serialize_function(
    func_visibility: str,
    func_return_type: str,
    func_name: str,
    func_parameters: List[str],
) -> Tuple[str, str]:
    """Returns a tuple of strings (class_attr_key, class_attr_value) where
class_attr_key is in the form: "[F:func_name]" and
class_attr_value is in the form "[func_visibility][func_return_type][param1type][param1name][param2type][param2name]...".
If no visibility was specified (func_visibility==""), then class_attr_value is "[][func_return_type][param1type][param1name][param2type][param2name]...".
If no parameters were specified (func_parameters==""), then class_attr_value is "[func_visibility][func_return_type]"."""

    func_visibility = func_visibility.strip()
    func_return_type = func_return_type.strip()
    func_name = func_name.strip()

    params: str = ""

    if func_parameters:
        for param in func_parameters:
            param_type: str = param.split(" ")[0].strip()
            param_name: str = param.split(" ")[1].strip()
            params += f"[{param_type}][{param_name}]"

    return (f"[F:{func_name}]", f"[{func_visibility}][{func_return_type}]{params}")


# ----------
# deserialize_variable


def deserialize_variable(
    class_attr_key: str, class_attr_value: str
) -> Tuple[str, str, str]:
    """Returns a tuple of strings containing the following variable information: (visibility, type, name).
If there is no visibility, the following is returned: ("", type, name)."""

    split_list: List[str] = class_attr_value.split("][")

    var_visibility: str = split_list[0][1:]
    var_type: str = split_list[1][:-1]

    var_name: str = class_attr_key[3:-1]

    return (var_visibility, var_type, var_name)


# ----------
# deserialize_function


def deserialize_function(
    class_attr_key: str, class_attr_value: str
) -> Tuple[str, str, str, List[str]]:
    """Returns a tuple of strings and a list of strings containing the
following function information: (visibility, return type, name, list of parameters).
If there is no visibility, the following is returned: ("", return type, name, list of parameters).
If there are no parameters, the following is returned: (visibility, return type, name, [])."""

    split_list: List[str] = class_attr_value[1:-1].split("][")

    func_visibility: str = split_list[0]
    func_return_type: str = split_list[1]

    func_name: str = class_attr_key[3:-1]

    param_list: List[str] = []

    for i in range(2, len(split_list), 2):
        param_list.append(f"{split_list[i]} {split_list[i+1]}")

    return (func_visibility, func_return_type, func_name, param_list)


# ----------
# parse_param_list


def parse_param_list(param_list_str: str) -> Optional[List[str]]:
    """Returns a valid parameter list (List[str] of format "['float x', 'int y', etc.]") on success, or None on failure.
Valid parameter lists are surrounded by brackets, contain no quotes, and no whitespace except between parameter types and names.
Variable names any types in the parameter list must contain no whitespace, no quotes, and not be surrounded by brackets.
Every variable in a valid parameter list must have a type and a name."""

    param_list_str = param_list_str.strip()

    # Check for start and end brackets and then shear them away
    if param_list_str.startswith("[") and param_list_str.endswith("]"):
        param_list_str = param_list_str[1:-1]
    else:
        return None

    # Split up the string into a list
    param_list: List[str] = param_list_str.split(",")

    # Check that every parameter has a type and a name
    for param in param_list:
        split_param: List[str] = param.split(" ")
        if len(split_param) != 2:
            return None
        if (
            parse_class_identifier(split_param[0]) is None
            or parse_class_identifier(split_param[1]) is None
        ):
            return None

    return param_list


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
