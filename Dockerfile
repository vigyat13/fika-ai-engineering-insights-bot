FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for matplotlib
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libfreetype6-dev \
    pkg-config \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Install pip dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Allow runtime CLI args like --owner, --repo
ENTRYPOINT ["python", "main.py"]
CMD []
