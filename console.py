#!/usr/bin/python3
"""
A command line interpreter for AirBnB clone
"""

import cmd
import re
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """A console class for the AirBnB-Clone project"""

    prompt: str = '(hbnb) '
    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Place': Place,
        'Amenity': Amenity,
        'Review': Review
    }

    @staticmethod
    def parse(arg, id_delimiter=" "):
        """
        Parse input arguments into a list
        Args:
            arg (str): The input arguments
            id_delimiter (str): Delimiter for splitting arguments
        Returns:
            list: List of parsed arguments
        """
        arg_list = arg.split(id_delimiter)
        return [x.strip() for x in arg_list if x]

    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True

    def help_quit(self):
        """
        Print help for the quit command
        """
        print("Quit command to exit the program\n")

    def do_EOF(self, arg):
        """
        EOF signal to exit the program
        """
        print("")
        return True

    def do_create(self, arg):
        """
        Create a new instance of a class, save it, and print its id
        """
        args = self.parse(arg)
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name in self.classes:
            new_instance = self.classes[class_name]()
            new_instance.save()
            print(new_instance.id)
        else:
            print("** class doesn't exist **")

    def help_create(self):
        """
        Print help for the create command
        """
        print("Create a new instance of a class, save it, and print its id")

    def do_show(self, arg):
        """
        Display the string representation of an instance
        based on the class name and id
        """
        args = self.parse(arg)
        if len(args) < 2:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name in self.classes:
            if len(args) < 2:
                print("** instance id missing **")
                return

            instance_id = args[1]
            key = "{}.{}".format(class_name, instance_id)
            instances = models.storage.all()

            if key in instances:
                print(instances[key])
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def help_show(self):
        """
        Print help for the show command
        """
        print("Display the string representation of an instance based on the class name and id")

    def do_destroy(self, arg):
        """
        Delete an instance based on the class name and id
        """
        args = self.parse(arg)
        if len(args) < 2:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name in self.classes:
            if len(args) < 2:
                print("** instance id missing **")
                return

            instance_id = args[1]
            key = "{}.{}".format(class_name, instance_id)
            instances = models.storage.all()

            if key in instances:
                del instances[key]
                models.storage.save()
            else:
                print("** no instance found **")
        else:
            print("** class doesn't exist **")

    def help_destroy(self):
        """
        Print help for the destroy command
        """
        print("Delete an instance based on the class name and id")

    def do_all(self, arg):
        """
        Print string representations of instances
        """
        args = self.parse(arg)
        instances = models.storage.all()

        if not args:
            print([str(value) for value in instances.values()])
        else:
            class_name = args[0]
            if class_name in self.classes:
                print([str(value) for value in instances.values() if isinstance(value, self.classes[class_name])])
            else:
                print("** class doesn't exist **")

    def help_all(self):
        """
        Print help for the all command
        """
        print("Print string representations of instances")

    def do_update(self, arg):
        """
        Update an instance's attribute value based on class name and id
        """
        args = self.parse(arg)
        if len(args) < 3:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args) < 4:
            print("** instance id missing **")
            return

        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        instances = models.storage.all()

        if key in instances:
            attribute_name = args[2]
            if len(args) < 5:
                print("** value missing **")
                return

            attribute_value = args[3]
            setattr(instances[key], attribute_name, attribute_value)
            instances[key].save()
        else:
            print("** no instance found **")

    def help_update(self):
        """
        Print help for the update command
        """
        print("Update an instance's attribute value based on class name and id")

    def do_count(self, arg):
        """
        Count the number of instances of a class
        """
        args = self.parse(arg)
        if not args:
            print("** class name missing **")
            return

        class_name = args[0]
        if class_name in self.classes:
            instances = models.storage.all()
            count = sum(1 for value in instances.values() if isinstance(value, self.classes[class_name]))
            print(count)
        else:
            print("** class doesn't exist **")

    def help_count(self):
        """
        Print help for the count command
        """
        print("Count the number of instances of a class")

    def emptyline(self):
        """
        Do nothing upon receiving an empty line
        """
        pass

    def default(self, line):
        """
        Custom default behavior for commands
        """
        parts = line.split('.')
        if len(parts) == 2:
            class_name = parts[0]
            if class_name in self.classes:
                if parts[1] == "all()":
                    self.do_all(class_name)
                elif parts[1] == "count()":
                    self.do_count(class_name)
                else:
                    cmd = parts[1].split('(')
                    if len(cmd) == 2 and cmd[1].endswith(')'):
                        if cmd[0] == "show":
                            self.do_show(f"{class_name} {cmd[1][1:-1]}")
                        elif cmd[0] == "destroy":
                            self.do_destroy(f"{class_name} {cmd[1][1:-1]}")
                        elif cmd[0] == "update":
                            self.do_update(f"{class_name} {cmd[1][1:-1]}")
                    else:
                        print("** invalid command **")
            else:
                print("** class doesn't exist **")
        else:
            print("** invalid command **")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
