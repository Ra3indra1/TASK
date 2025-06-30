# Use official Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole application into the container
COPY . .

# Expose port 5000 for Flask app
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]