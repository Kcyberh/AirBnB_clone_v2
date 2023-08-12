#!/usr/bin/python3

import cmd
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.user import User
from models import storage

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
        """Retrieve an instance based on its ID"""
        args_list = args.split()
        if not args_list:
            print("** class name missing **")
            return

        try:
            class_name = args_list[0]
            if class_name in self.classes:
                if len(args_list) < 2:
                    print("** instance id missing **")
                    return

                instance_id = args_list[1]
                key = "{}.{}".format(class_name, instance_id)
                instances = storage.all()

                if key in instances:
                    print(instances[key])
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")

    def do_destroy(self, args):
        """Destroy an instance based on its ID"""
        args_list = args.split()
        if not args_list:
            print("** class name missing **")
            return

        try:
            class_name = args_list[0]
            if class_name in self.classes:
                if len(args_list) < 2:
                    print("** instance id missing **")
                    return

                instance_id = args_list[1]
                key = "{}.{}".format(class_name, instance_id)
                instances = storage.all()

                if key in instances:
                    del instances[key]
                    storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")

    def do_all(self, args):
        """Print string representation of instances (User or BaseModel)"""
        instances = storage.all()
        if not args:
            print([str(value) for value in instances.values()])
        else:
            args_list = args.split()
            class_name = args_list[0]
            if class_name in self.classes:
                print([str(value) for value in instances.values() if isinstance(value, self.classes[class_name])])
            else:
                print("** class doesn't exist **")

    def do_update(self, args):
        """Update an instance's attribute value based on class name and id or dictionary"""
        args_list = args.split()
        if not args_list:
            print("** class name missing **")
            return

        try:
            class_name = args_list[0]
            if class_name not in self.classes:
                print("** class doesn't exist **")
                return

            if len(args_list) < 2:
                print("** instance id missing **")
                return

            instance_id = args_list[1]
            key = "{}.{}".format(class_name, instance_id)
            instances = storage.all()

            if key in instances:
                if len(args_list) < 3:
                    print("** attribute name missing **")
                    return

                if args_list[2] == "{" and args_list[-1] == "}":
                    try:
                        update_dict = eval(' '.join(args_list[2:]))
                        for k, v in update_dict.items():
                            setattr(instances[key], k, v)
                        instances[key].save()
                    except Exception:
                        print("** invalid dictionary **")
                        return
                else:
                    if len(args_list) < 4:
                        print("** value missing **")
                        return

                    attribute_name = args_list[2]
                    attribute_value = args_list[3]
                    setattr(instances[key], attribute_name, attribute_value)
                    instances[key].save()
            else:
                print("** no instance found **")
        except IndexError:
            print("** instance id missing **")

    def do_count(self, args):
        """Count the number of instances of a class"""
        args_list = args.split()
        if not args_list:
            print("** class name missing **")
            return

        try:
            class_name = args_list[0]
            if class_name in self.classes:
                instances = storage.all()
                count = sum(1 for value in instances.values() if isinstance(value, self.classes[class_name]))
                print(count)
            else:
                print("** class doesn't exist **")
        except IndexError:
            print("** class name missing **")

    def default(self, line):
        """Custom default behavior for commands"""
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
