# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app/

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV PYTHONUNBUFFERED 1

# Run the FastAPI app with Uvicorn on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

