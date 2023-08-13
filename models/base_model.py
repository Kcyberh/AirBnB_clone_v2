#!/usr/bin/python3
"""
Defines the BaseModel class.
"""

import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
    Represents the BaseModel of the HBnB project.
    Attributes:
        id (str): Unique identifier.
        created_at (datetime): Creation date and time.
        updated_at (datetime): Last update date and time.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new BaseModel instance.
        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        tform = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()

        # If kwargs are provided, set instance attributes
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, tform)
                else:
                    self.__dict__[key] = value
        else:
            # For new instances, add to the storage
            models.storage.new(self)

    def save(self):
        """Update updated_at with the current datetime and save to storage."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        Convert the BaseModel instance to a dictionary.
        Returns:
            dict: Dictionary representation of the instance.
        """
        rdict = self.__dict__.copy()
        rdict["created_at"] = self.created_at.isoformat()
        rdict["updated_at"] = self.updated_at.isoformat()
        rdict["__class__"] = self.__class__.__name__
        return rdict

    def __str__(self):
        """
        Return a string representation of the BaseModel instance.
        Returns:
            str: Formatted string representation.
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
