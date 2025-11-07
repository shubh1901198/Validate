# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies (if any)
RUN pip install --upgrade pip

# Run the Python script
CMD ["python", "vehicle_dashboard.py"]
