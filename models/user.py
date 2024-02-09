#!/usr/bin/python3
from models.base_model import BaseModel


class User(BaseModel):
    """
    User class represents a user in the system.

    Attributes:
        email (str): The email address of the user.
        password (str): The password associated with the user account.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """
    email: str = ""
    password: str = ""
    first_name: str = ""
    last_name: str = ""
