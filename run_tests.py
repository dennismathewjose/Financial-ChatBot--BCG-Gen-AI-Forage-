import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import your tests
from tests.test_pipeline import TestPipeline  # Adjust class name if needed

# Run tests
if __name__ == "__main__":
    unittest.main()
