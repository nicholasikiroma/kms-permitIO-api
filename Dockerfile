# Use a specific Python image tag
FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libffi-dev \
    build-essential


# Set the working directory in the container to root
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the project dependencies with verbose output
RUN pip install --no-cache-dir --verbose -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["fastapi", "run"]