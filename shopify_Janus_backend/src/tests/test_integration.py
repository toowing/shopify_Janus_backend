"""Integration tests"""
import unittest
import requests
from ..clients.janus_client import JanusClient
from ..config import Config

class TestIntegration(unittest.TestCase):
    """Integration test cases"""
    
    @classmethod
    def setUpClass(cls):
        cls.api_url = f"http://127.0.0.1:{Config.PORT}/api/generate-image"
        cls.janus_client = JanusClient()
    
    def test_image_generation_flow(self):
        """Test complete image generation flow"""
        test_prompt = "A beautiful sunset over mountains"
        
        # Test direct client
        result = self.janus_client.generate_image(test_prompt)
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['image_url'])
        
        # Test API endpoint
        response = requests.post(
            self.api_url,
            json={"prompt": test_prompt},
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['image_url'])

    def test_error_handling(self):
        """Test error handling scenarios"""
        test_cases = [
            {"input": "", "expected_status": 400},
            {"input": None, "expected_status": 400},
            {"input": "   ", "expected_status": 400},
        ]
        
        for case in test_cases:
            response = requests.post(
                self.api_url,
                json={"prompt": case["input"]},
                headers={"Content-Type": "application/json"}
            )
            self.assertEqual(
                response.status_code, 
                case["expected_status"], 
                f"Failed for input: {case['input']}"
            )

if __name__ == '__main__':
    unittest.main() 