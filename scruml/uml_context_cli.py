#ScruML                                                                         
#uml_context_cli.py                                                                       
#Team JJARS                                                                     

import cmd
from scruml.uml_diagram import UMLDiagram
umld: UMLDiagram = UMLDiagram()

class uml_context_cli(cmd.Cmd):

  def do_exit(self, inp):
    print ("Exited")
    return True

  def do_add_class(self, inp):
    """add_class [class name]                                                   
Adds new class if one with that name does not already exist"""  
    add_class_name: str = umld.add_class(inp)
    if add_class_name == None:
      print ("'{}' class already exists".format(inp))
    else:
      print("Added '{}' class".format(inp))
  
  def do_remove_class(self, inp):
    """remove_class [class name]                                                
Removes class if it exists"""
    remove_class_name: str = umld.remove_class(inp)
    if remove_class_name == None:
      print ("'{}' class does not exist".format(inp))
    else:
      print("Removed '{}' class".format(inp))
  
  def do_list_classes(self,inp):
    """Lists all classes"""
    print("Listing all classes:")
    class_names: List[str] = umld.get_all_class_names()
    print('\n'.join(class_names))
  
  def do_rename_class(self, inp):
    """rename_class [class name] [new class name]                               
Changes name of class if one of that name exists"""
    names: str = inp.split()
    umld.rename_class(names[0], names[1])
    print("changing "+names[0]+" to "+names[1])
  
  def do_save(self, inp):
    """Saves UML diagram"""
  
  def do_load(self, inp):
    """load [filename]
Loads existing UML diagram"""
    print ("Loading '{}'".format(inp))   
                                                      
  def activate():
    uml_context_cli().cmdloop()