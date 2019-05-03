#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestCountGet(unittest.TestCase):
    """Test count and get methods of db_storage"""
    def test_count(self):
        """Test count method for all classes"""
        count = models.storage.count()
        amenity = Amenity(name="Hot Tub")
        amenity.save()
        self.assertEqual(models.storage.count(), count + 1)
        state = State(name="Coruscant")
        state.save()
        self.assertEqual(models.storage.count(), count + 2)
        city = City(name="Galactic City", state_id=state.id)
        city.save()
        self.assertEqual(models.storage.count(), count + 3)
        user = User(name="caroldanvers",
                    email="cap@616.marvel",
                    password="tesseract")
        user.save()
        self.assertEqual(models.storage.count(), count + 4)
        place = Place(name="The Batcave", city_id=city.id, user_id=user.id)
        place.save()
        self.assertEqual(models.storage.count(), count + 5)
        review = Review(name="5 stars",
                        user_id=user.id,
                        place_id=place.id,
                        text="AWESOME!")
        review.save()
        self.assertEqual(models.storage.count(), count + 6)

    def test_get(self):
        """Test get method for all classes"""
        amenity = Amenity(name="AC")
        amenity.save()
        self.assertEqual(amenity, models.storage.get("Amenity", amenity.id))
        state = State(name="Coruscant")
        state.save()
        city = City(name="Galactic City", state_id=state.id)
        city.save()
        self.assertEqual(city, models.storage.get("City", city.id))
        user = User(name="caroldanvers",
                    email="cap@616.marvel",
                    password="tesseract")
        user.save()
        place = Place(name="The Batcave", city_id=city.id, user_id=user.id)
        place.save()
        self.assertEqual(place, models.storage.get("Place", place.id))
        review = Review(name="5 stars",
                        user_id=user.id,
                        place_id=place.id,
                        text="AWESOME!")
        review.save()
        self.assertEqual(review, models.storage.get("Review", review.id))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))
