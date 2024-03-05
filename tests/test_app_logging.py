import os
import sys
import unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from app_logging import find_project_root_folder


class TestAppLogging(unittest.TestCase):
    def test_find_project_root_folder(self):
        current_path = os.path.abspath(__file__)
        expected_root_folder = os.path.dirname(os.path.dirname(current_path))
        actual_root_folder = find_project_root_folder(current_path)
        self.assertEqual(actual_root_folder, expected_root_folder)

    def test_find_project_root_folder_raises_error(self):
        current_path = "/path/to/nonexistent/file"
        with self.assertRaises(RuntimeError):
            find_project_root_folder(current_path)


if __name__ == "__main__":
    unittest.main()

if __name__ == "__main__":
    unittest.main()
