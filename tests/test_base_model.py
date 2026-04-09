import unittest
from datetime import datetime

from app.models.base_model import Base


class TestBaseModel(unittest.TestCase):
    def test_created_at_default_is_callable(self):
        self.assertTrue(callable(Base.createdAt.default.arg))
        self.assertIs(Base.createdAt.default.arg, datetime.now)

    def test_updated_at_default_and_onupdate_are_callable(self):
        self.assertTrue(callable(Base.updatedAt.default.arg))
        self.assertIs(Base.updatedAt.default.arg, datetime.now)
        self.assertTrue(callable(Base.updatedAt.onupdate.arg))
        self.assertIs(Base.updatedAt.onupdate.arg, datetime.now)


if __name__ == "__main__":
    unittest.main()
