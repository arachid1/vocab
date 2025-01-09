# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files first to leverage Docker's caching mechanism
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry install --no-root 

# Copy the rest of the backend source code
COPY . .

# Expose the port used by Django
EXPOSE 8000

# Add the startup script to the container
COPY startup_script.sh /app/startup_script.sh
RUN chmod +x /app/startup_script.sh

# Run the startup script and then start the Django development server
CMD ["/bin/sh", "-c", "/app/startup_script.sh && poetry run python manage.py runserver 0.0.0.0:8000"]