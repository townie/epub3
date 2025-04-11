"""Main test file for epub3 package."""

import unittest

import epub3


class TestExample(unittest.TestCase):
    """Simple test case to verify test setup."""

    def test_version(self):
        """Test that version is set correctly."""
        self.assertTrue(hasattr(epub3, "__version__"))
        self.assertIsInstance(epub3.__version__, str)


if __name__ == "__main__":
    unittest.main()
