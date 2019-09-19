#ScruML                                                                         
#repl.py                                                                        
#Team JJARS                                                                     

from cmd import Cmd

class MyPrompt(Cmd):
  def do_exit(self, inp):
    print ("Exited")
    return True

  def do_add_class(self, inp):
    """add_class [class name]                                                   
Adds new class if one with that name does not already exist"""
    print("Added '{}' class".format(inp))
  
  def do_remove_class(self, inp):
    """remove_class [class name]                                                
Removes class if it exists"""
    print("Removed '{}' class".format(inp))
  
  def do_list_classes(self,inp):
    """Lists all classes"""
    print("Listing all classes:\n")
  
  def do_rename_class(self, inp):
    """rename_class [class name] [new class name]                               
Changes name of class if one of that name exists"""
    names = inp.split()
    print("changing "+names[0]+" to "+names[1])
  
  def do_save(self, inp):
    """Saves UML diagram"""
  
  def do_load(self, inp):
    """load [filename]
Loads existing UML diagram"""
    print ("Loading '{}'".format(inp))                                                           

MyPrompt().cmdloop()


