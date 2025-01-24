# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Install necessary system dependencies for Chrome and Selenium
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -y install -f \
    && rm google-chrome-stable_current_amd64.deb




    
# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application using Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
