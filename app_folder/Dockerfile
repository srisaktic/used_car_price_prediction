FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

# XGBoost runtime + build tools for wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgomp1 build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install deps first for better caching
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code + model artifacts
COPY . .

# Container will listen on 8000 (host port is set via -p)
EXPOSE 8000

# Start API (use 0.0.0.0 in containers)
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]