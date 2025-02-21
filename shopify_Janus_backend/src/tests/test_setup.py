import unittest
import os
from dotenv import load_dotenv
from gradio_client import Client

class TestSetup(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        
    def test_env_variables(self):
        """Test if all required environment variables are set"""
        required_vars = [
            'HUGGINGFACE_API_KEY',
            'JANUS_MODEL_ID',
            'SHOPIFY_SHOP_NAME',
            'SHOPIFY_ADMIN_ACCESS_TOKEN',
            'SHOPIFY_STOREFRONT_TOKEN'
        ]
        
        for var in required_vars:
            self.assertIsNotNone(
                os.getenv(var), 
                f"Environment variable {var} is not set"
            )
            
    def test_gradio_connection(self):
        """Test if we can connect to the Gradio API"""
        try:
            client = Client("deepseek-ai/Janus-Pro-7B")
            self.assertIsNotNone(client)
        except Exception as e:
            self.fail(f"Failed to connect to Gradio API: {str(e)}")

    def test_environment_variables(self):
        """Test if all required environment variables are set"""
        required_vars = [
            'HUGGINGFACE_API_KEY',
            'JANUS_MODEL_ID',
        ]
        
        for var in required_vars:
            self.assertIsNotNone(
                os.getenv(var), 
                f"Environment variable {var} is not set"
            )

if __name__ == '__main__':
    unittest.main() 