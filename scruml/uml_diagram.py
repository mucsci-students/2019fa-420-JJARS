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
RelationshipDict = Dict[str, AttributeDict]


class UMLDiagram(yaml.YAMLObject):
    def __init__(self) -> None:
        self.__classes: Dict[str, AttributeDict] = dict()
        self.__relationships: Dict[ClassPair, RelationshipDict] = dict()

    # ----------
    # Class functions

    def add_class(self, class_name: str) -> Optional[str]:
        if class_name in self.__classes:
            return None
        self.__classes[class_name] = dict()
        return class_name

    def remove_class(self, class_name: str) -> Optional[str]:
        if class_name not in self.__classes:
            return None
        del self.__classes[class_name]
        # TODO: Implement removing a class and all of its relationships
        return class_name

    def get_all_class_names(self) -> List[str]:
        return list(self.__classes.keys())

    def rename_class(self, old_class_name: str, new_class_name: str) -> Optional[str]:
        if old_class_name not in self.__classes or new_class_name in self.__classes:
            return None
        self.__classes[new_class_name] = self.__classes.pop(old_class_name)
        # TODO: change relationships that reference this class
        return new_class_name

    # ----------
    # Class attribute functions

    def set_class_attribute(
        self, class_name: str, attribute_name: str, attribute_value: str
    ) -> Optional[str]:
        if class_name not in self.__classes:
            return None
        self.__classes[class_name][attribute_name] = attribute_value
        return attribute_value

    def remove_class_attribute(
        self, class_name: str, attribute_name: str
    ) -> Optional[str]:
        if (
            class_name not in self.__classes
            or attribute_name not in self.__classes[class_name]
        ):
            return None
        del self.__classes[class_name][attribute_name]
        return attribute_name

    def get_class_attributes(self, class_name: str) -> Optional[AttributeDict]:
        if class_name not in self.__classes:
            return None
        return self.__classes[class_name]

    # ----------
    # Relationship functions

    def add_relationship(
        self,
        class_name_a: str,
        class_name_b: str,
        relationship_name: Optional[str] = None,
    ) -> bool:
        class_pair: ClassPair = (class_name_a, class_name_b)
        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
            or relationship_name in self.__relationships[class_pair]
        ):
            return False
        self.__relationships[class_pair][relationship_name] = AttributeDict()
        return True

    def remove_relationship(
        self,
        class_name_a: str,
        class_name_b: str,
        relationship_name: Optional[str] = None,
    ) -> bool:
        class_pair: ClassPair = (class_name_a, class_name_b)
        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
            or relationship_name not in self.__relationships[class_pair]
        ):
            return False
        del self.__relationships[class_pair][relationship_name]
        return True

    def get_relationships_between(
        self, class_name_a: str, class_name_b: str
    ) -> Optional[RelationshipDict]:
        class_pair: ClassPair = (class_name_a, class_name_b)
        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
        ):
            return None
        return self.__relationships[class_pair]

    def get_all_relationship_pairs(self) -> List[ClassPair]:
        return list(self.__relationships.keys())

    # ----------
    # Relationship attribute functions

    # TODO
