# Use the official lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY stream.py stream.py

# Expose the port Flask is running on
EXPOSE 8000

# Command to run the Flask app
CMD ["python", "stream.py", "--port=8000"]

