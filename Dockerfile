FROM python:3.11-slim

WORKDIR /app

# Install system dependencies if required by torch/scipy (optional, but good for data science packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything into the working directory
COPY . .

# Expose the API port
EXPOSE 8001

# Run the API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]
