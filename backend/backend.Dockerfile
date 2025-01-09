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

# # Run the Django development server (for local development only)
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["sleep", "infinity"]