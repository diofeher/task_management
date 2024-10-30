# Base image - use official, minimal image for Python
FROM python:3.12-slim as base

# Use a non-root user for security
RUN addgroup --system appgroup && adduser --system --group appuser

# Set the working directory
WORKDIR /app

# Copy the requirements file separately to leverage Docker's cache
COPY requirements.lock pyproject.toml README.md /app/

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.lock

# Activate virtual environment and install app dependencies
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code to the working directory
COPY . .

# Use unprivileged user
USER appuser

# Expose the application port
EXPOSE 8000

# Entrypoint to run the FastAPI application
CMD ["uvicorn", "src.main:app"]
# Security hardening
# - Use slim image and avoid installing unnecessary packages
# - Run as a non-root user
# - Avoid caching pip packages
# - Use ENV to configure virtual environment for secure package isolation
