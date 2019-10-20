# ScrUML
# uml_diagram.py
# Team JJARS
from typing import Dict
from typing import FrozenSet
from typing import List
from typing import Optional
from typing import Tuple

import yaml

ClassPair = FrozenSet[str]
RelationshipName = Optional[str]
RelationshipID = Tuple[ClassPair, RelationshipName]

AttributeDict = Dict[str, str]
RelationshipDict = Dict[str, AttributeDict]


class UMLDiagram(yaml.YAMLObject):
    def __init__(self) -> None:
        self.__classes: Dict[str, AttributeDict] = dict()
        self.__relationships: Dict[RelationshipID, RelationshipDict] = dict()

    def add_class(self, class_name: str) -> Optional[str]:
        if class_name in self.__classes:
            return None
        self.__classes[class_name] = dict()
        return class_name

    def remove_class(self, class_name: str) -> Optional[str]:
        if class_name not in self.__classes:
            return None
        del self.__classes[class_name]
        return class_name

    # TODO: Implement removing a class and all of its relationships
    def complete_remove(self, class_name: str) -> Optional[str]:
        pass

    def get_all_class_names(self) -> List[str]:
        return list(self.__classes.keys())

    def rename_class(self, old_class_name: str, new_class_name: str) -> Optional[str]:
        if old_class_name not in self.__classes or new_class_name in self.__classes:
            return None
        self.__classes[new_class_name] = self.__classes.pop(old_class_name)
        return new_class_name

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

    def add_relationship(
        self,
        class_name_a: str,
        class_name_b: str,
        relationship_name: RelationshipName = None,
    ) -> Optional[RelationshipID]:
        rel_id: RelationshipID = (
            frozenset((class_name_a, class_name_b)),
            relationship_name,
        )
        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or rel_id in self.__relationships
        ):
            return None
        self.__relationships[rel_id] = dict()
        return rel_id

    def remove_relationship(
        self,
        class_name_a: str,
        class_name_b: str,
        relationship_name: RelationshipName = None,
    ) -> Optional[RelationshipID]:
        rel_id: RelationshipID = (
            frozenset((class_name_a, class_name_b)),
            relationship_name,
        )
        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or rel_id not in self.__relationships
        ):
            return None
        del self.__relationships[rel_id]
        return rel_id
