# ScrUML
# uml_diagram.py
# Team JJARS

from typing import Optional, Dict, List

class UMLDiagram:

    def __init__(self) -> None:
        self.__classes: Dict[str, Dict[str, str]] = dict()
        self.__relationships: Dict[Frozenset[str], Dict[str, Dict[str, str]]] = dict()

    def add_class(class_name: str) -> Optional[str]:
        if class_name in self.__classes:
            return None
        self.__classes[class_name] = dict()

    def remove_class(class_name: str) -> Optional[str]:
        if class_name not in self.__classes:
            return None
        del self.__classes[class_name]

    def get_all_class_names() -> List[str]:
        return list(self.__classes.keys())

    def rename_class(old_class_name: str, new_class_name: str) -> Optional[str]:
        if old_class_name not in self.__classes or new_class_name in self.__classes:
            return None
        self.__classes[new_class_name] = self.__classes.pop(old_class_name)
        return new_class_name
