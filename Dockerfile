FROM python:3.11-slim

WORKDIR /app

# System dependencies required by newspaper3k
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy full project
COPY . /app

# Install python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Create directories used by the app
RUN mkdir -p data/trips
RUN mkdir -p data/vector_db

# Expose API port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]