#!/usr/bin/python3
"""
A python program called console.py that contains
the entry point of the command interpreter
"""
import cmd
import shlex
import re
import ast
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    HBNBCommand class provides a simple command-line interface
    for creating, managing, and interacting with instances of
    different classes like BaseModel.
    """
    prompt = "(hbnb)"
    valid_classes = [
            "BaseModel",
            "User",
            "State",
            "City",
            "Place",
            "Amenity",
            "Review"
    ]

    def emptyline(self):
        """
        Do nothing when an empty line is entered.
        """
        pass

    def do_quit(self, arg):
        """
        Quit command to exit the program
        Usage: quit
        """
        return True

    def help_quit(self):
        """
        Help message for the quit command.
        """
        print("Quit command to exit the program")

    def do_EOF(self, line):
        """
        Handle the End-of-File condition.
        """
        return True

    def do_create(self, arg):
        """
        Create a new instance of BaseModel and save it
        to the JSON file.
        Usage: create <class name>
        """
        commands = shlex.split(arg)
        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(f"{commands[0]}()")
            storage.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Show the string representation of an instance
        Usage: show <class name> <instance id>
        """
        commands = shlex.split(arg)
        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Delete an instance.
        Usage: destroy <class name> <instance id>
        """
        commands = shlex.split(arg)

        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
        Print the string representation of all instances
        or a specific class.
        Usage: all[class name]
        """
        objects = storage.all()
        commands = shlex.split(arg)
        if len(commands) == 0:
            for key, value in objects.items():
                print(str(value))
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            for key, value in objects.items():
                if key.split('.')[0] == commands[0]:
                    print(str(value))

    def default(self, arg):
        """
        Define default
        """
        arg_list = arg.split('.')
        incoming_class_name = arg_list[0]
        command = arg_list[1].split('(')
        incoming_method = command[0]
        incoming_xtra_arg = command[1].split(')')[0]
        method_dict = {
                'all': self.do_all,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update,
                'count': self.do_count
        }
        if incoming_method in method_dict.keys():
            if incoming_method != "update":
                return method_dict[incoming_method]("{} {}".format(
                    incoming_class_name, incoming_xtra_arg))
            else:
                return method_dict[incoming_method]("{} {} {} {}".format(
                    incoming_class_name,
                    obj_id))
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_count(self, arg):
        """
        Define do_count
        """
        objects = storage.all()
        commands = shlex.split(arg)
        incoming_class_name = commands[0]
        count = 0
        if commands:
            if incoming_class_name in self.valid_classes:
                for obj in objects.values():
                    if obj.__class__.__name__ == incoming_class_name:
                        count += 1
                print(count)
            else:
                print("** invalid class name **")
        else:
            print("** class name missing **")

    def do_update(self, arg):
        """
        Update an instance by adding or updating
        an attribute.
        Usage: update <class name> <id> <attribute_name>
        <attribute_value>
        """
        commands = shlex.split(arg)
        if len(commands) == 0:
            print("** class name missing **")
        elif commands[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(commands) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(commands[0], commands[1])
            if key not in objects:
                print("** no instance found **")
            elif len(commands) < 3:
                print("** attribute name missing **")
            elif len(commands) < 4:
                print("** value missing **")
            else:
                obj = objects[key]
                curly_braces = re.search(r"\{(.*?)\}", arg)
                if curly_braces:
                    str_data = curly_braces.group(1)
                    arg_dict = ast.literal_eval("{" + str_data + "}")
                    attribute_names = list(arg_dict.keys())
                    attribute_values = list(arg_dict.values())
                    attr_name1 = attribute_names[0]
                    attr_value1 = attribute_values[0]
                    attr_name2 = attribute_names[1]
                    attr_value2 = attribute_values[1]
                    setattr(obj, attr_name1, attr_value1)
                    setattr(obj, attr_name2, attr_value2)
                else:
                    attr_name = commands[2]
                    attr_value = commands[3]
                    try:
                        attr_value = eval(attr_value)
                    except Exception:
                        pass
                    setattr(obj, attr_name, attr_value)
                obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
