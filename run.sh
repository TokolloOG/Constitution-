#!/bin/bash
echo "Starting Heavenet API..."
docker build -t heavenet-api .
docker run -p 5000:5000 heavenet-api
