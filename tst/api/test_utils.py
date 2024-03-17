import unittest
from datetime import datetime
from utils import is_valid_email, text_to_dict, get_datetime_from_string

class TestFunctions(unittest.TestCase):

    def test_is_valid_email(self):
        self.assertTrue(is_valid_email("test@example.com"))  # Valid email
        self.assertFalse(is_valid_email("testexample.com"))  # Invalid email
        self.assertTrue(is_valid_email("USER@EXAMPLE.COM"))  # Email with uppercase letters
        self.assertFalse(is_valid_email("test@example"))  # Email with invalid domain

    def test_text_to_dict(self):
        self.assertEqual(text_to_dict("name: John\nage: 30\ngender: Male"),
                         {'name': 'John', 'age': '30', 'gender': 'Male'})  # Valid text input
        self.assertEqual(text_to_dict("name: John\nage: null\ngender: Male"),
                         {'name': 'John', 'age': None, 'gender': 'Male'})  # Text input with null values
        self.assertEqual(text_to_dict("This is a test."), {})  # Text input with no key-value pairs

    def test_get_datetime_from_string(self):
        self.assertEqual(get_datetime_from_string("2024-03-16 12:00:00"),
                         datetime(2024, 3, 16, 12, 0))  # Valid date string
        with self.assertRaises(ValueError):
            get_datetime_from_string("16-03-2024 12:00:00")  # Invalid date format
        self.assertEqual(get_datetime_from_string("2024-03-16 08:30:00"),
                         datetime(2024, 3, 16, 8, 30))  # Date string with different time format
        self.assertEqual(get_datetime_from_string("2025-12-31 23:59:59"),
                         datetime(2025, 12, 31, 23, 59, 59))  # Date string with future date

if __name__ == '__main__':
    unittest.main()
