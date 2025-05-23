FROM python:3.10-slim

# Install LibreOffice and dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    libxrender1 \
    libxext6 \
    libsm6 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files and install Python deps
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Run FastAPI app on default port
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
