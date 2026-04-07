# # ui/Dockerfile
# FROM python:3.11-slim

# WORKDIR /app

# # Install only what the UI needs
# COPY requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt

# # Copy UI code (and optional .streamlit/config.toml)
# COPY . .

# # Compose DNS will resolve "api" → API container
# ENV API_URL=http://api:8000

# EXPOSE 8501
# CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]


# inside ui/Dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY streamlit_app.py ./

# (optional but recommended) copy config into the place Streamlit expects
COPY .streamlit /root/.streamlit

EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]