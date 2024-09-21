FROM python:3.11-slim


# Set the working directory
WORKDIR /app

# Install postgresql-client
RUN apt-get update && apt-get install -y libpq-dev

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .


# Run the application
CMD ["fastapi", "run", "app/main.py", "--port", "80"]


