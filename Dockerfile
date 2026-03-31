FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Flask typically runs on 5000, but 8080 is fine for AWS/Azure
EXPOSE 8080

# For Flask, use Gunicorn for production-grade performance
# Install it via: RUN pip install gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]