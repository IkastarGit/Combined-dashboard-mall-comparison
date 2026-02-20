FROM python:3.11-slim

# Install system dependencies and Chrome in a single layer to minimize image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget ca-certificates gnupg curl unzip \
    libu2f-udev \
    libglib2.0-0 libnss3 libnspr4 libdbus-1-3 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxcb1 libxkbcommon0 libx11-6 \
    libxcomposite1 libxdamage1 libxext6 libxfixes3 \
    libxrandr2 libgbm1 libpango-1.0-0 libcairo2 \
    libasound2 libatspi2.0-0 libgtk-3-0 \
    libx11-xcb1 libxi6 libxtst6 libxrender1 \
    fonts-liberation fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome Stable
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends ./google-chrome-stable_current_amd64.deb \
    && rm -f google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV CHROME_BIN=/usr/bin/google-chrome
ENV PYTHONUNBUFFERED=1
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null
ENV SE_CACHE_PATH=/tmp/selenium

WORKDIR /app

# Install Python dependencies (cached as separate layer)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --timeout=120 -r requirements.txt

# Copy application code
COPY . .

# Verify Chrome is installed
RUN google-chrome --version

EXPOSE 8501

CMD streamlit run main_ui.py \
    --server.port ${PORT:-8501} \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false
