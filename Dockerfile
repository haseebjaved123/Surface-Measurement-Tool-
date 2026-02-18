# For Hugging Face Spaces (Docker) and any Docker-based deployment
FROM python:3.11-slim

WORKDIR /app

# System deps for OpenCV and PaddlePaddle
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Create dirs that app expects
RUN mkdir -p input_images output_images processed_images results Dataset

ENV PORT=7860
EXPOSE 7860

# HF Spaces and many hosts set PORT in env
CMD gunicorn -b 0.0.0.0:${PORT:-7860} --timeout 300 server:app
