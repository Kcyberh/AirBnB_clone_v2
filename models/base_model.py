#!/bin/usr/python3
"""file containing basemodel class"""
from datetime import datetime
import models
import uuid

class BaseModel:
    def __init__(self, *args, **kwargs):
        """Initialize BaseModel attributes"""

        if kwargs is None or len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    time = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, time)
                elif key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """ Class method to display in human readable BaseModel instance """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """Save the instance to storage and update updated_at"""
        self.updated_at = datetime.now()
        storage.save()

    def __init__(self, *args, **kwargs):
        if kwargs:
            # ... (existing code)

            # If it's a new instance, add a call to the new method on storage
            if 'id' not in kwargs:
                storage.new(self)






