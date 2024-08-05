# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Copy backend source code
COPY . .

# Command to run the FastAPI server
CMD ["python", "main.py"]
