FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Ensure FastAPI and uvicorn are included in your requirements.txt or install them directly
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r requirements.txt

EXPOSE 8501 8000

# Update the health check command
HEALTHCHECK CMD curl --fail http://localhost:8000/_stcore/health || exit 1

# Add a custom script to start both Streamlit and FastAPI
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

ENTRYPOINT ["/app/start.sh"]
