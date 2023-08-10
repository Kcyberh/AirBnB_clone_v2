#!/bin/usr/python3

import cmd
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.user import User

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    classes = {
        'Amenity': Amenity,
        'BaseModel': BaseModel,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State,
        'User': User
    }
    def do_quit(self, args):
        """Exit the program"""
        return True

    def do_EOF(self, args):
        """Exit the program"""
        print("")  # Print a newline before exiting
        return True

    def help_quit(self):
        print("Exit the program")

    def help_EOF(self):
        print("Exit the program")

    
    def do_create(self, args):
        """Create a new instance of User or BaseModel, save it, and print id"""
        if not args:
            print("** class name missing **")
            return

        try:
            new_instance = eval(args)()
            new_instance.save()
            print(new_instance.id)
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, args):
        """Print the string representation of an instance (User or BaseModel)"""
        args_list = args.split()
        if not args_list:
            print("** class name missing **")
            return

        try:
            class_name = args_list[0]
            instance_id = args_list[1]
            key = "{}.{}".format(class_name, instance_id)
            if key in models.storage.all():
                print(models.storage.all()[key])
            else:
                print("** no instance found **")
        except IndexError:
            if args_list[0] not in models.class_names:
                print("** class doesn't exist **")
            else:
                print("** instance id missing **")

    def do_destroy(self, args):
        """Delete an instance (User or BaseModel) based on class name and id"""
        args_list = args.split()
        if not args_list:
            print("** class name missing **")
            return

        try:
            class_name = args_list[0]
            instance_id = args_list[1]
            key = "{}.{}".format(class_name, instance_id)
            if key in models.storage.all():
                del models.storage.all()[key]
                models.storage.save()
            else:
                print("** no instance found **")
        except IndexError:
            if args_list[0] not in models.class_names:
                print("** class doesn't exist **")
            else:
                print("** instance id missing **")

    def do_all(self, args):
        """Print string representation of instances (User or BaseModel)"""
        instances = self.classes[args] if args in self.classes else None

        if instances is None:
            print("** class doesn't exist **")
            return

        print([str(value) for key, value in instances.items()])

    def do_update(self, args):
        """Update an instance's attribute value based on class name and id"""
        args_list = args.split()
        if not args_list:
            print("** class name missing **")
            return

        try:
            class_name = args_list[0]
            instance_id = args_list[1]
            key = "{}.{}".format(class_name, instance_id)
            if key not in models.storage.all():
                print("** no instance found **")
                return

            if len(args_list) < 3:
                print("** attribute name missing **")
                return

            if len(args_list) < 4:
                print("** value missing **")
                return

            if args_list[0] not in models.class_names:
                print("** class doesn't exist **")
                return

            attribute_name = args_list[2]
            if attribute_name in ["id", "created_at", "updated_at"]:
                print("** cannot update reserved attribute **")
                return

            if hasattr(models.storage.all()[key], attribute_name):
                attribute_type = type(getattr(models.storage.all()[key], attribute_name))
                try:
                    attribute_value = attribute_type(args_list[3])
                except ValueError:
                    print("** invalid value **")
                    return
                setattr(models.storage.all()[key], attribute_name, attribute_value)
                models.storage.all()[key].save()
            else:
                print("** attribute doesn't exist **")

        except IndexError:
            print("** instance id missing **")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
