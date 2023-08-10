#!/bin/usr/python3

import json
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place

class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        return FileStorage.__objects

    def new(self, obj):
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        serialized_objects = {key: obj.to_dict() for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, 'w') as file:
            json.dump(serialized_objects, file)

    def reload(self):
        if path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r') as file:
                serialized_objects = json.load(file)
                for key, value in serialized_objects.items():
                    class_name = value['__class__']
                    obj = eval(class_name)(**value)
                    FileStorage.__objects[key] = obj
def _serialize_instance(self, obj):
        """Serialize an instance to a dictionary"""
        if isinstance(obj, User):
            return {
                "__class__": obj.__class__.__name__,
                "id": obj.id,
                "created_at": obj.created_at.isoformat(),
                "updated_at": obj.updated_at.isoformat(),
                "email": obj.email,
                "password": obj.password,
                "first_name": obj.first_name,
                "last_name": obj.last_name
            }

def _deserialize_instance(self, obj_dict):
        """Deserialize a dictionary to an instance"""
        class_name = obj_dict.get("__class__")
        if class_name == "User":
            return User(**obj_dict)
