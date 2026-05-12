import unittest
from datetime import datetime

from app.models.base_model import Base


class TestBaseModel(unittest.TestCase):
    def test_created_at_default_is_callable(self):
        self.assertTrue(callable(Base.created_at.default.arg))
        self.assertIs(Base.created_at.default.arg, datetime.now)

    def test_updated_at_default_and_onupdate_are_callable(self):
        self.assertTrue(callable(Base.updated_at.default.arg))
        self.assertIs(Base.updated_at.default.arg, datetime.now)
        self.assertTrue(callable(Base.updated_at.onupdate.arg))
        self.assertIs(Base.updated_at.onupdate.arg, datetime.now)


if __name__ == "__main__":
    unittest.main()
