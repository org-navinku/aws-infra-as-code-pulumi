import unittest
import pulumi
from pulumi.runtime import mocks
import importlib.util
import os

class TestS3Bucket(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the main.py module dynamically
        spec = importlib.util.spec_from_file_location(
            "main",
            os.path.join(os.path.dirname(__file__), "../__main__.py")
        )
        cls.main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.main)

    def setUp(self):
        # Set up Pulumi mocks before each test
        self.mocks = mocks.MockResourceMonitor()
        pulumi.runtime.set_mocks(self.mocks)
    
    def test_bucket_creation(self):
        # Run the Pulumi program
        outputs = pulumi.runtime.run(self.main)
        
        # Verify the bucket was created
        self.assertIn("my-bucket", self.mocks.resources)
        self.assertEqual(self.mocks.resources["my-bucket"]["type"], "aws:s3/bucketV2:BucketV2")
        
        # Verify exports
        self.assertIn("bucket_name", outputs)
        self.assertEqual(outputs["bucket_name"], "my-bucket")

    def test_bucket_properties(self):
        # Run the Pulumi program
        pulumi.runtime.run(self.main)
        
        # Verify bucket properties
        bucket = self.mocks.resources["my-bucket"]
        self.assertEqual(bucket["props"]["tags"], {})
        self.assertFalse(bucket["props"]["forceDestroy"])

    def tearDown(self):
        # Clean up after each test
        pulumi.runtime.reset_options()

if __name__ == "__main__":
    unittest.main()