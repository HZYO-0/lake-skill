FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY cli/ cli/
COPY skills/ skills/
COPY config.default.yaml .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Create directories
RUN mkdir -p input work kb reports examples

# Set entrypoint
ENTRYPOINT ["lake-skill"]

# Default command
CMD ["--help"]
