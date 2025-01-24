# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive


# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application using Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
