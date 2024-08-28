FROM python:3.11-slim

# ARGS
#By default, the application will run in production mode
ARG MODE=run

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .


# Run the application
CMD ["fastapi", "run", "app/main.py", "--port", "80"]


