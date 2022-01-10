import unittest
from seating.student import Student, DummyStudent, is_dummy_student


class TestStudent(unittest.TestCase):
    def test_dummy_student(self):
        self.assertEqual(DummyStudent().get_real(), False)

    def test_is_dummy_student(self):
        self.assertTrue(is_dummy_student(DummyStudent()))


if __name__ == '__main__':
    unittest.main()