FROM python:3.11-slim

# Install system dependencies (for Tkinter if needed, though containers are usually headless)
RUN apt-get update && apt-get install -y \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variable for display if using X11 (optional)
# ENV DISPLAY=host.docker.internal:0

# Default command
CMD ["python", "main.py"]
