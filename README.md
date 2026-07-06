# Heavenet API - 12 Laws Verification

A Flask-based API that validates requests against 12 constitutional laws. Each request must pass all laws to be approved.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and set your real `HEAVENET_API_KEY`:
   ```
   HEAVENET_API_KEY=your_real_secret_key
   FLASK_PORT=5000
   ```

## Run Locally (Development)

Start the API server in debug mode:
```bash
python main.py
```

The API will run on `http://localhost:5000`

Health check endpoint:
```bash
curl http://localhost:5000/health
```

## Run in Production

Use Gunicorn for production deployment:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 wsgi:app
```

Or with additional options:
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 60 wsgi:app
```

## API Endpoint

### POST /verify

Validates a request against all 12 laws.

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "api_key": "your_key",
  "user_id": 1,
  "action": "read",
  "ip": "127.0.0.1",
  "user_agent": "Mozilla/5.0",
  "timestamp": 1609459200
}
```

**Success Response (200):**
```json
{
  "status": "approved",
  "message": "All 12 laws passed",
  "timestamp": "2026-06-10T12:30:45.123456"
}
```

**Failure Response (400):**
```json
{
  "status": "rejected",
  "failed_laws": [2, 5],
  "timestamp": "2026-06-10T12:30:45.123456"
}
```

## The 12 Laws

| Law | Rule | Description |
|-----|------|-------------|
| 1 | Required Fields | `api_key`, `user_id`, `action`, `ip`, and `timestamp` must be present |
| 2 | API Key Validation | API key must match `HEAVENET_API_KEY` from environment |
| 3 | User ID Format | User ID must be a positive integer |
| 4 | Timestamp Freshness | Timestamp must not be older than 5 minutes |
| 5 | IP Whitelist | IP must be `127.0.0.1` (localhost only) |
| 6-12 | Placeholder Laws | Reserved for future constitutional rules |

## Testing

Run the automated test suite:
```bash
python test_laws.py
```

This will:
- Start the Flask server automatically
- Run 4 test cases:
  - **Test A:** Valid request → expect 200 + "approved"
  - **Test B:** Missing api_key → expect 400 + Law 1 error
  - **Test C:** Wrong api_key → expect 400 + Law 2 error
  - **Test D:** Wrong IP "8.8.8.8" → expect 400 + Law 5 error
- Print detailed results for each test
- Automatically kill the server

## Docker

### Build the image:
```bash
docker build -t heavenet-api .
```

### Run the container (Development):
```bash
docker run -p 5000:5000 --env-file .env heavenet-api
```

### Run the container (Production):
```bash
docker run -d -p 5000:5000 --env-file .env --name heavenet-api heavenet-api
```

### Docker Compose (optional):
```bash
docker-compose up
```

## Project Structure

```
heavenet/
├── main.py                 # Flask app entry point
├── wsgi.py                # WSGI entry point for production
├── test_laws.py           # Automated test suite
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
├── .gitignore            # Git ignore configuration
├── Dockerfile            # Docker configuration
├── README.md             # This file
└── heavenet/
    └── laws/
        ├── law1.py       # Required fields check
        ├── law2.py       # API key validation
        ├── law3.py       # User ID validation
        ├── law4.py       # Timestamp freshness
        ├── law5.py       # IP whitelist
        ├── law6.py       # Placeholder
        ├── law7.py       # Placeholder
        ├── law8.py       # Placeholder
        ├── law9.py       # Placeholder
        ├── law10.py      # Placeholder
        ├── law11.py      # Placeholder
        └── law12.py      # Placeholder
```

## Example Usage

### Using curl:
```bash
curl -X POST http://localhost:5000/verify \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "heavenet-secret-123",
    "user_id": 1,
    "action": "read",
    "ip": "127.0.0.1",
    "user_agent": "Mozilla/5.0",
    "timestamp": 1609459200
  }'
```

### Using Python:
```python
import requests

data = {
    "api_key": "heavenet-secret-123",
    "user_id": 1,
    "action": "read",
    "ip": "127.0.0.1",
    "user_agent": "Mozilla/5.0",
    "timestamp": 1609459200
}

response = requests.post("http://localhost:5000/verify", json=data)
print(response.json())
```

## Troubleshooting

**Port already in use:**
```bash
# Change port in .env
FLASK_PORT=5001
```

**Connection refused:**
- Make sure the server is running: `python main.py`
- Check that port 5000 is not blocked by firewall

**API key rejected:**
- Verify the `HEAVENET_API_KEY` in `.env` matches your request
- Copy `.env.example` to `.env` and set your real secret key

**Gunicorn workers not responding:**
- Increase the timeout: `--timeout 120`
- Reduce workers if system has low resources: `--workers 2`

## Logging

The API logs all requests and validation results. Check logs in:
- **Development:** Console output
- **Production:** Configure log handlers as needed

Log entries include:
- Request IP address
- Which laws passed/failed
- Error messages and exceptions

## License

MIT License - See LICENSE file for details

## Oath

**I will uphold Law I-VII or I will fork.**

---

For more information, visit [Heavenet Constitution](https://github.com/TokolloOG/Constitution-)
# 🌐 HeavenET

A production-ready starter project. No secrets, no real keys - built entirely for local dev.

## Stack
- **Backend**: Python Flask
- **Crypto**: Node.js TweetNaCl + BS58
- **Testing**: pytest

## Requirements
- Python 3.7+
- Node.js 14+
- pip
- npm

## Installation & Setup

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt