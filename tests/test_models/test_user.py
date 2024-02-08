import os
import unittest
import models
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):

    def setUp(self):
        """
        Create a temporary test file
        for saving data.
        """
        self.test_file = "test_file.json"
        models.storage.__file_path = self.test_file
        models.storage.save()

    def tearDown(self):
        """
        Remove the temporary test
        file after the test
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_user_attributes(self):
        """
        Create a new User instance
        """
        test_user = User()
        self.assertEqual(test_user.email, "")
        self.assertEqual(test_user.password, "")
        self.assertEqual(test_user.first_name, "")
        self.assertEqual(test_user.last_name, "")

    def test_user_inherits_from_base_model(self):
        """
        Creates a User instance
        """
        test_user = User()
        self.assertTrue(issubclass(User, BaseModel))

    def test_user_str_representation(self):
        """
        Create a new User instance
        """
        test_user = User()
        test_user.email = "waiganjo@gmail.com"
        test_user.password = "Root@"
        test_user.first_name = "Elijah"
        test_user.last_name = "Waiganjo"
        user_str = str(test_str)
        self.assertIn("User", user_str)
        self.assertIn("waiganjo@gmail.com", user_str)
        self.assertIn("Elijah", user_str)
        self.assertIn("Waiganjo", user_str)

    def test_user_to_dict(self):
        """
        Create a new User instance
        """
        test_user = User()
        test_user.email = "waiganjo@gmail.com"
        test_user.first_name = "Elijah"
        test_user.last_name = "Waiganjo"
        test_user.save()
        user_dict = test_user.to_dict()
        self.assertEqual(user_dict['email'], "waiganjo@gmail.com")
        self.assertEqual(user_dict['first_name'], "Elijah")
        self.assertEqual(user_dict['last_name'], "Waiganjo")

    def test_user_instance_creation(self):
        """
        Create a new User instance with arguments
        """
        test_user = User(
                email="waiganjo@gmail.com", password="Root@", first_name="Elijah" last_name="Waiganjo"
        )
        self.assertEqual(test_user.email, "waiganjo@gmail.com")
        self.assertEqual(test_user.password, "Root@")
        self.assertEqual(test_user.first_name, "Elijah")
        self.assertEqual(test_user.last_name, "Waiganjo")

    def test_user_instance_to_dict(self):
        """
        Create a new User instance with specific attribute values
        """
        test_user = User(
                email="waiganjo@gmail.com", password="Root@", first_name="Elijah" last_name="Waiganjo"
        )
        user_dict = test_user.to_dict()
        self.assertEqual(user_dict['email'], "waiganjo@gmail.com")
        self.assertEqual(user_dict['password'], "Root@")
        self.assertEqual(user_dict['first_name'], "Elijah")
        self.assertEqual(user_dict['last_name'], "Waiganjo")

    def test_user_id_generation(self):
        """
        Create two different User instances
        """
        test_user = User()
        user2 = User()
        self.assertNotEqual(test_user.id, user2.id)

    if __name__ == '__main__':
        unittest.main()
