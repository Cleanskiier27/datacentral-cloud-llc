FROM python:3.11-slim

# Install system dependencies, OpenJDK 17, Maven, and Google Cloud SDK
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y build-essential \
    python3-tk \
    openjdk-21-jdk \
    maven \
    curl \
    gnupg \
    libpcsclite-dev \
    swig \
    && mkdir -p /usr/share/keyrings \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && apt-get update && apt-get install -y google-cloud-cli \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

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
