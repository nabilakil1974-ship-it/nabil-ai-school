"""Regression tests for the factory's separated safety layer.

Run: python -m unittest scripts.nabil_factory.factory.test_locked_v18_safety
"""
import unittest
from scripts.nabil_factory.factory.locked_v18_safety import (
    SafetyContractViolation, assert_safe_factory_boundaries,
    assert_source_identity, assert_verified_publication,
    verify_rational_arithmetic,
)

class LockedSafetyTests(unittest.TestCase):
    def test_contracts(self):
        assert_safe_factory_boundaries()

    def test_source_identity(self):
        assert_source_identity({"lesson_id": "G07-MATH-001", "book_id": "real-pdf"}, "real-pdf")
        with self.assertRaises(SafetyContractViolation):
            assert_source_identity({"lesson_id": "G07-MATH-001", "book_id": "wrong"}, "real-pdf")

    def test_unreviewed_is_not_verified(self):
        with self.assertRaises(SafetyContractViolation):
            assert_verified_publication(quality_passed=True,
                                        scientific_status="UNREVIEWED",
                                        upload_verified=True)

    def test_cannot_publish_without_verified_upload(self):
        with self.assertRaises(SafetyContractViolation):
            assert_verified_publication(quality_passed=True,
                                        scientific_status="VERIFIED",
                                        upload_verified=False)

    def test_exact_fractions(self):
        verify_rational_arithmetic(1, 2, 2, 4)
        with self.assertRaises(SafetyContractViolation):
            verify_rational_arithmetic(67 * 100, 1, 100, 1)

if __name__ == "__main__":
    unittest.main()
