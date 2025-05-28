# Dockerfile for Esami PEF
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . ./

# Create instance and backups directories
RUN mkdir -p instance backups

# Expose the Flask port
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Start the Flask development server
CMD ["flask", "run", "--port", "5000"]
