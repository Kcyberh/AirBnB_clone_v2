#!/usr/bin/python3
"""
Defines the FileStorage class.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """Represents an abstracted storage engine for managing object data.
    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary of objects (__objects)."""
        return FileStorage.__objects

    def new(self, obj):
        """Adds a new object to __objects with key '<obj_class_name>.id'.
        Args:
            obj (BaseModel): The object to add.
        """
        obj_key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[obj_key] = obj

    def save(self):
        """Serializes __objects to JSON format and saves it to __file_path."""
        serialized_objects = {
            key: value.to_dict() for key, value in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, "w") as file:
            json.dump(serialized_objects, file)

    def reload(self):
        """Deserializes JSON data from __file_path and populates __objects."""
        try:
            with open(FileStorage.__file_path, "r") as file:
                loaded_data = json.load(file)
                for key, value in loaded_data.items():
                    cls_name = value["__class__"]
                    del value["__class__"]
                    self.new(eval(cls_name)(**value))
        except FileNotFoundError:
            return
