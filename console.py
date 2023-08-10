#!/bin/usr/python3

import cmd

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

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

if __name__ == "__main__":
    HBNBCommand().cmdloop()



