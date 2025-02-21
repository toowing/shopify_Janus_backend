"""Test runner for the application"""
import unittest
import sys
import logging
from src.tests.test_setup import TestSetup
from src.tests.test_integration import TestIntegration
from src.config import Config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_all_tests():
    """Run all test cases"""
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSetup))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    logger.info("Starting tests...")
    
    # Check if Flask server is running
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', Config.PORT))
    if result != 0:
        logger.error("Flask server is not running! Please start the server first.")
        sys.exit(1)
    
    # Run tests
    success = run_all_tests()
    
    if not success:
        logger.error("Some tests failed!")
        sys.exit(1)
    else:
        logger.info("All tests passed!") 