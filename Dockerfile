# Deploying on top of official Python 3.13 slim bookworm layer
FROM python:3.13-slim

# Establish the path context inside the virtual environment
WORKDIR /app

# Install system utilities essential for processing raw NLP compilation structures
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# PRODUCTION OPTIMIZATION: Explicitly install the CPU-only version of PyTorch.
# This prevents Docker from pulling down 4GB+ of useless NVIDIA GPU CUDA drivers.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Copy configuration maps first to optimize layer caching efficiency
COPY requirements.txt .

# Execute isolated dependency installation routines (will skip torch since it is already installed)
RUN pip install --no-cache-dir -r requirements.txt

# Bake the Stanza Urdu machine learning binaries straight into the image asset
RUN python -c "import stanza; stanza.download('ur', processors='tokenize,pos,ner', verbose=False)"

# Shift rest of your application code into the image workspace
COPY . .

# Setup an unprivileged user space context to bypass root privileges vulnerabilities
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Document the designated target runtime port allocation
EXPOSE 8082

# Ignite execution framework passing via dynamic parameters mapping
CMD ["python", "main.py"]