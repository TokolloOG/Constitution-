FROM python:3.11-slim
WORKDIR /app
COPY .env .env
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "main.py"]
