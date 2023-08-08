#!/bin/usr/python3
"""file containing basemodel class"""
from datetime import datetime
import models
import uuid

Class BaseModel():
    def __init__(self, *args, **kwargs):
        """ Class Base Model, Base model for the AirBnB Clone"""
         if kwargs is None or len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        
         else:
             
             
