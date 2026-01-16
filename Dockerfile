FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy project definition
COPY pyproject.toml .

# Copy source code and config
COPY src/ ./src/
COPY searxng/ ./searxng/
COPY Modelfile .

# Install dependencies
RUN pip install .

# Expose the Chainlit UI port
EXPOSE 8000

# Start the Chainlit Web Server
CMD ["chainlit", "run", "src/app.py", "--host", "0.0.0.0", "--port", "8000", "--headless"]