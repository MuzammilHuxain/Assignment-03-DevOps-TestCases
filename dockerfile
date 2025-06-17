# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    chromium-driver \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Set display port to avoid errors
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy requirements and test script
COPY requirements.txt .
COPY selenium_test.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run test script
CMD ["python", "selenium_test.py"]
