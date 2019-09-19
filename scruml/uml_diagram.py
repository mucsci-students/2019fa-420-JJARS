# ScrUML
# uml_diagram.py
# Team JJARS

class UMLDiagram:

    def __init__() -> None:
        self.__class_list: Dict[str, Dict[str, str]] = dict()
        self.__relationship_list: Dict[Frozenset[str], Dict[str, Dict[str, str]]] = dict()

    def add_class(class_name: str) -> Optional[str]:
        if class_name in self.__class_list:
            return None
        self.__class_list[class_name] = dict()

    def remove_class(class_name: str) -> Optional[str]:
        if class_name not in self.__class_list:
            return None
        del self.__class_list[class_name]

    def get_all_class_names() -> List[str]:
        return list(self.__class_list.keys())

    def rename_class(old_class_name: str, new_class_name: str) -> Optional[str]:
        if old_class_name not in self.__class_list or new_class_name in self.__class_list:
            return None
        self.__class_list[new_class_name] = self.__class_list.pop(old_class_name)
        return new_class_name
