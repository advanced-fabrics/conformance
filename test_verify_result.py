import unittest

from verify_result import verify


class ResultTests(unittest.TestCase):
    def test_rejects_mutable_identity(self):
        self.assertIn(
            "digest must be immutable sha256",
            verify({"schemaVersion": "conformance.advfab.org/v1", "suite": "v1.0", "digest": "latest", "tests": [{}]}),
        )

    def test_skip_requires_reason(self):
        errors = verify({
            "schemaVersion": "conformance.advfab.org/v1",
            "suite": "v1.0",
            "digest": "sha256:" + "0" * 64,
            "tests": [{"id": "provider.swap", "status": "skip"}],
        })
        self.assertIn("skip requires reason for provider.swap", errors)


if __name__ == "__main__":
    unittest.main()
