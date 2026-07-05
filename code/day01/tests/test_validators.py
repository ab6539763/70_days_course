"""Day 1 validators 单元测试。"""

import unittest

from src.validators import validate_age, validate_motto, validate_non_empty


class TestValidators(unittest.TestCase):
    def test_non_empty_ok(self):
        ok, err = validate_non_empty("张三", "姓名")
        self.assertTrue(ok)
        self.assertEqual(err, "")

    def test_non_empty_fail(self):
        ok, err = validate_non_empty("   ", "姓名")
        self.assertFalse(ok)
        self.assertIn("不能为空", err)

    def test_age_ok(self):
        ok, age, err = validate_age("28")
        self.assertTrue(ok)
        self.assertEqual(age, 28)

    def test_age_not_digit(self):
        ok, age, err = validate_age("abc")
        self.assertFalse(ok)
        self.assertIsNone(age)

    def test_motto_too_long(self):
        ok, _, err = validate_motto("a" * 201)
        self.assertFalse(ok)


if __name__ == "__main__":
    unittest.main()
