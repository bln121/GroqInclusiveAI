# Use a Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the backend code to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
