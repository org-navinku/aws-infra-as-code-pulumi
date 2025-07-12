import unittest
import pulumi
from pulumi.runtime import mocks
import os

class TestS3Bucket(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize Pulumi mocks
        cls.mocks = mocks.MockResourceMonitor()
        pulumi.runtime.set_mocks(cls.mocks)
        
        # Import the program to test
        cls.program = cls._load_program()

    @classmethod
    def _load_program(cls):
        """Helper to import the Pulumi program"""
        import sys
        from pathlib import Path
        
        # Add project directory to path
        project_dir = str(Path(__file__).parent.parent)
        if project_dir not in sys.path:
            sys.path.insert(0, project_dir)
            
        # Import the program module
        import __main__ as program
        return program

    def setUp(self):
        # Reset mocks before each test
        self.mocks.clear()
        pulumi.runtime.reset_options()

    def test_bucket_creation(self):
        # Run the program
        pulumi.runtime.run(self.program)
        
        # Verify bucket was created
        self.assertIn("my-bucket", self.mocks.resources)
        self.assertEqual(
            self.mocks.resources["my-bucket"]["type"],
            "aws:s3/bucketV2:BucketV2"
        )

    def test_bucket_properties(self):
        # Run the program
        pulumi.runtime.run(self.program)
        
        # Check bucket properties
        bucket = self.mocks.resources["my-bucket"]
        self.assertEqual(bucket["props"]["tags"], {})
        self.assertFalse(bucket["props"]["forceDestroy"])

    def tearDown(self):
        # Clean up after each test
        pulumi.runtime.reset_options()

if __name__ == "__main__":
    unittest.main()