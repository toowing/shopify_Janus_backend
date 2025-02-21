"""Main Flask application"""
from flask import Flask, request, jsonify
from typing import Tuple, Dict, Any
from .clients.janus_client import JanusClient, logger
from .config import Config

app = Flask(__name__)

class APIServer:
    """API Server implementation"""
    
    def __init__(self):
        self.janus_client = JanusClient()
    
    def validate_request(self, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validate incoming request data"""
        if not data:
            return False, "Empty request"
        if 'prompt' not in data:
            return False, "Missing 'prompt' field"
        if not isinstance(data['prompt'], str):
            return False, "Prompt must be a string"
        return True, ""
    
    def handle_generate_image(self):
        """Handle image generation request"""
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Invalid JSON'}), 400
            
            is_valid, error = self.validate_request(data)
            if not is_valid:
                return jsonify({'error': error}), 400
            
            prompt = data['prompt'].strip()
            if not prompt:
                return jsonify({'error': 'Please provide a text description'}), 400
            
            try:
                result = self.janus_client.generate_image(prompt)
                return jsonify(result)
            except Exception as e:
                error_msg = str(e)
                if "GPU quota" in error_msg:
                    return jsonify({
                        'error': 'Service temporarily unavailable due to high demand.',
                        'details': error_msg
                    }), 503
                raise
            
        except ValueError as ve:
            logger.error(f"Validation error: {str(ve)}")
            return jsonify({'error': str(ve)}), 400
        except Exception as e:
            logger.error(f"API error: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

# Initialize API server
api_server = APIServer()

# Route definitions
@app.route("/")
def home():
    """Home endpoint"""
    return jsonify({"message": "Welcome to the Shopify + Janus API!"})

@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    """Image generation endpoint"""
    return api_server.handle_generate_image()

def run_server():
    """Run the Flask server"""
    ports = [Config.PORT, 8080, 5000]
    
    for port in ports:
        try:
            logger.info(f"Attempting to start server on port {port}...")
            app.run(host=Config.HOST, debug=True, port=port)
            break
        except Exception as e:
            logger.error(f"Failed to start server on port {port}: {e}")
    else:
        raise Exception("Failed to start server on any port")

if __name__ == '__main__':
    run_server()