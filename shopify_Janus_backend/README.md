# Shopify + Janus Image Generation API

A Flask API that integrates Shopify Storefront with Janus-Pro-7B for AI image generation.

## Features
- AI image generation using Janus-Pro-7B
- RESTful API endpoints
- Automatic retry mechanism for GPU quota
- Environment-based configuration
- Docker support

## Prerequisites
- Python 3.9+
- Hugging Face API key
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd shopify-janus-backend
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Local Development
```bash
# Start the Flask server
python -m src.app

# Run tests
python run_tests.py
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up --build
```

## API Endpoints

### Generate Image
```bash
POST /api/generate-image
Content-Type: application/json

{
    "prompt": "A beautiful sunset over mountains"
}
```

## Configuration

Environment variables in `.env`:
- `HUGGINGFACE_API_KEY`: Your Hugging Face API key
- `JANUS_MODEL_ID`: Model ID (default: deepseek-ai/Janus-Pro-7B)
- `ENVIRONMENT`: development/production
- `PORT`: Server port (default: 9999)

## Project Structure
```
.
├── src/
│   ├── clients/          # API clients
│   ├── tests/           # Test suite
│   ├── app.py           # Flask application
│   └── config.py        # Configuration
├── .env                 # Environment variables
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose config
└── run_tests.py       # Test runner
```

## Testing
- Unit tests and integration tests included
- Run with `python run_tests.py`
- Requires Flask server to be running

## Error Handling
- Automatic retry for GPU quota limits
- Graceful error responses
- Environment-specific configurations

## Author
[Ellie Yeung]