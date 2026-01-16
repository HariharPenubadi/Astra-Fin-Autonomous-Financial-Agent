FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .

COPY src/ ./src/
COPY searxng/ ./searxng/
COPY Modelfile .

RUN pip install .
RUN pip install fastapi uvicorn pydantic python-dotenv

# Expose the API Port
EXPOSE 8000

CMD ["python", "-m", "src.server"]