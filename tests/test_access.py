import unittest
from src.models.user import Student, Professor


class TestAccessLevels(unittest.TestCase):
    def test_roles_hierarchy(self):
        st = Student("1", "Test Student", "s@test.com", "CS", 1)
        pr = Professor("2", "Test Prof", "p@test.com", "CS")
        self.assertLess(st.get_access_level(), pr.get_access_level())


if __name__ == "__main__":
    unittest.main()