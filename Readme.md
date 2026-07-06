# HeaveneT

A cryptographic signing and verification system using TweetNaCl for secure transactions.

## Project Structure

- **Python Backend**: Flask server with cryptographic verification
  - `server.py` - Flask HTTP server
  - `main.py` - Main entry point
  - `client.py` - Client library for interactions
  - `tests/` - Pytest test suite

- **JavaScript Frontend**: Web interface with crypto signing
  - `index.html` - Main interface
  - `keys.html` - Key management interface
  - JS crypto modules using TweetNaCl and BS58 encoding

## Prerequisites

- Python 3.11 or higher
- Node.js 18+ and npm

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/TokolloOG/heavenet.git
cd heavenet