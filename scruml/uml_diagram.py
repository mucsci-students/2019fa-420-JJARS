# ScrUML
# uml_diagram.py
# Team JJARS
from typing import Dict
from typing import FrozenSet
from typing import List
from typing import Optional
from typing import Tuple

import yaml

ClassPair = Tuple[str, str]

AttributeDict = Dict[str, str]
RelationshipDict = Dict[Optional[str], AttributeDict]

# ----------
# UMLDiagram class

# TODO: Change return types, they are causing issues


class UMLDiagram:
    """Interactive model representing a UML diagram containing relationships and classes with attributes."""

    # ----------
    # Constructor

    def __init__(self) -> None:
        self.__classes: Dict[str, AttributeDict] = dict()
        self.__relationships: Dict[ClassPair, RelationshipDict] = dict()

    # ----------
    # Class functions

    # ----------
    # add_class

    def add_class(self, class_name: str) -> Optional[str]:
        """Adds a class with name 'class_name' to the diagram.
Fails if a class with 'class_name' is already present in the diagram.
Returns 'class_name' on success, or 'None' on failure."""

        if class_name in self.__classes:
            return None

        self.__classes[class_name] = dict()

        return class_name

    # ----------
    # remove_class

    def remove_class(self, class_name: str) -> Optional[str]:
        """Removes the class with name 'class_name' from the diagram.
Fails if a class with 'class_name' is not present in the diagram.
Returns 'class_name' on success, or 'None' on failure."""

        if class_name not in self.__classes:
            return None

        del self.__classes[class_name]

        # Remove all relationships that refer to this class
        # (We work on a copy to avoid working on a dictionary while iterating over it)
        new_relationships: Dict[
            ClassPair, RelationshipDict
        ] = self.__relationships.copy()
        for class_pair in self.__relationships:
            if class_name in class_pair:
                del new_relationships[class_pair]
        self.__relationships = new_relationships

        return class_name

    # ----------
    # get_all_class_names

    def get_all_class_names(self) -> List[str]:
        """Returns a 'List[str]' containing the name of every class in the diagram."""

        return list(self.__classes.keys())

    # ----------
    # rename_class

    def rename_class(self, old_class_name: str, new_class_name: str) -> Optional[str]:
        """Renames the class with name 'old_name' to 'new_name' in the diagram.
Fails if a class with 'old_name' is not present in the diagram or a class with 'new_name' already exists in the diagram.
Returns 'new_name' on success or 'None' on failure."""

        if old_class_name not in self.__classes or new_class_name in self.__classes:
            return None

        self.__classes[new_class_name] = self.__classes.pop(old_class_name)

        # Update all relationships that refer to this class
        for class_pair in self.__relationships:
            if old_class_name in class_pair:
                new_class_pair: Tuple[str, str] = (
                    class_pair[0]
                    if class_pair[0] != old_class_name
                    else new_class_name,
                    class_pair[1]
                    if class_pair[1] != old_class_name
                    else new_class_name,
                )
                self.__relationships[new_class_pair] = self.__relationships.pop(
                    class_pair
                )

        return new_class_name

    # ----------
    # Class attribute functions

    # ----------
    # set_class_attribute

    def set_class_attribute(
        self, class_name: str, attribute_name: str, attribute_value: str
    ) -> Optional[str]:
        """Sets the value of 'attribute_name' to 'attribute_value' for the class with name 'class_name' in the diagram.
If the class does not yet have an attribute with the name 'attribute_name', one will be created.
Fails if a class with 'class_name' is not present in the diagram.
Returns 'attribute_value' on success, or 'None' on failure."""

        if class_name not in self.__classes:
            return None

        self.__classes[class_name][attribute_name] = attribute_value

        return attribute_value

    # ----------
    # remove_class_attribute

    def remove_class_attribute(
        self, class_name: str, attribute_name: str
    ) -> Optional[str]:
        """Removes the attribute with name 'attribute_name' from class 'class_name'.
Fails if an attribute with 'attribute_name' is not found in 'class_name'.
Fails if a class with 'class_name' is not present in the diagram.
Returns 'attribute_name' on success, or 'None' on failure."""

        if (
            class_name not in self.__classes
            or attribute_name not in self.__classes[class_name]
        ):
            return None

        del self.__classes[class_name][attribute_name]

        return attribute_name

    # ----------
    # get_class_attributes

    def get_class_attributes(self, class_name: str) -> Optional[AttributeDict]:
        """Returns a Dict[str, str] containing the attribute names and values for class 'class_name'.
Fails and returns 'None' if a class with 'class_name' is not present in the diagram."""

        if class_name not in self.__classes:
            return None

        return self.__classes[class_name]

    # ----------
    # Relationship functions

    # ----------
    # __resolve_class_pair

    def __resolve_class_pair(self, class_name_a: str, class_name_b: str) -> ClassPair:
        """Returns (class_name_b, class_name_a) if that key exists as a pair in the diagram.
Otherwise, returns (class_name_a, class_name_b)."""

        class_pair: ClassPair = (class_name_a, class_name_b)

        # If the reverse of the current pair exists already, just use that
        if (class_name_b, class_name_a) in self.__relationships:
            class_pair = (class_name_b, class_name_a)

        return class_pair

    # ----------
    # add_relationship

    def add_relationship(
        self,
        class_name_a: str,
        class_name_b: str,
        relationship_name: Optional[str] = None,
    ) -> bool:
        """Adds a relationship between the classes 'class_name_a' and 'class_name_b' with optional 'relationship_name' to the diagram.
Fails if a relation between the classes 'class_name_a' and 'class_name_b' with optional 'relationship_name' is already present in the diagram.
Returns 'True' on success, or 'False' on failure."""

        class_pair: ClassPair = self.__resolve_class_pair(class_name_a, class_name_b)

        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or (
                class_pair in self.__relationships
                and relationship_name in self.__relationships[class_pair]
            )
        ):
            return False

        if class_pair not in self.__relationships:
            self.__relationships[class_pair] = {}

        self.__relationships[class_pair][relationship_name] = {}

        return True

    # ----------
    # remove_relationship

    def remove_relationship(
        self,
        class_name_a: str,
        class_name_b: str,
        relationship_name: Optional[str] = None,
    ) -> bool:
        """Removes the relationship between the classes 'class_name_a' and 'class_name_b' with optional 'relationship_name' from the diagram.
Fails if a relationship between the classes 'class_name_a' and 'class_name_b' with optional 'relationship_name' is not present in the diagram.
Returns 'True' on success, or 'False' on failure."""

        class_pair: ClassPair = self.__resolve_class_pair(class_name_a, class_name_b)

        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
            or relationship_name not in self.__relationships[class_pair]
        ):
            return False

        del self.__relationships[class_pair][relationship_name]

        if self.__relationships[class_pair] == {}:
            del self.__relationships[class_pair]

        return True

    # ----------
    # get_relationships_between

    def get_relationships_between(
        self, class_name_a: str, class_name_b: str
    ) -> Optional[RelationshipDict]:
        """Returns a Dict[Optional[str], Dict[str, str]] containing every relationship (with attributes) between 'class_name_a' and 'class_name_b'.
Fails if class 'class_name_a' or class 'class_name_b' is not present in the diagram.
Fails if a relationship between 'class_name_a' and 'class_name_b' does not exist.
Returns 'None' on failure."""

        class_pair: ClassPair = self.__resolve_class_pair(class_name_a, class_name_b)

        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
        ):
            return None

        return self.__relationships[class_pair]

    # ----------
    # get_all_relationship_pairs

    def get_all_relationship_pairs(self) -> List[ClassPair]:
        """Returns a 'List[Tuple[str, str]]' containing every pair of related classes in the diagram."""

        return list(self.__relationships.keys())

    # ----------
    # Relationship attribute functions

    # ----------
    # set_relationship_attribute

    # TODO: Design consideration - Should there be an optional parameter in middle of the parameter list?
    def set_relationship_attribute(
        self,
        class_name_a: str,
        class_name_b: str,
        relationship_name: Optional[str],
        attribute_name: str,
        attribute_value: str,
    ) -> Optional[str]:
        """Sets the value of 'attribute_name' to 'attribute_value' for the relationship between 'class_name_a' and 'class_name_b'
with the optional name 'relationship_name'.
If the relationship does not yet have an attribute with the name 'attribute_name', one will be created.
Fails if a relationship with 'class_name_a', 'class_name_b', and 'relationship_name' is not present in the diagram.
Returns 'attribute_value' on success, or 'None' on failure."""

        class_pair: ClassPair = self.__resolve_class_pair(class_name_a, class_name_b)

        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
            or relationship_name not in self.__relationships[class_pair]
        ):
            return None

        self.__relationships[class_pair][relationship_name][
            attribute_name
        ] = attribute_value

        return attribute_value

    # ----------
    # remove_relationship_attribute

    # TODO: Design consideration - Should there be an optional parameter in middle of the parameter list?
    def remove_relationship_attribute(
        self,
        class_name_a: str,
        class_name_b: str,
        relationship_name: Optional[str],
        attribute_name: str,
    ) -> Optional[str]:
        """Removes the attribute with name 'attribute_name' from the relationship between 'class_name_a' and 'class_name_b'
with the optional name 'relationship_name'.
Fails if an attribute with 'attribute_name' is not found in the relationship.
Fails if a relationship with 'class_name_a', 'class_name_b', and 'relationship_name' is not present in the diagram.
Returns 'attribute_name' on success, or 'None' on failure."""

        class_pair: ClassPair = self.__resolve_class_pair(class_name_a, class_name_b)

        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
            or relationship_name not in self.__relationships[class_pair]
            or attribute_name not in self.__relationships[class_pair][relationship_name]
        ):
            return None

        del self.__relationships[class_pair][relationship_name][attribute_name]

        return attribute_name

    # ----------
    # get_relationship_attributes

    def get_relationship_attributes(
        self, class_name_a: str, class_name_b: str, relationship_name: Optional[str]
    ) -> Optional[AttributeDict]:
        """Returns a Dict[str, str] containing the attribute names and values for the relationship between 'class_name_a' and 'class_name_b'
with the optional name 'relationship_name'.
Fails and returns 'None' if a relationship with 'class_name_a', 'class_name_b', and 'relationship_name' is not present in the diagram."""
        # TODO: Implement this
        return None
