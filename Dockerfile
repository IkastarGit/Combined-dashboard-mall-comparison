FROM python:3.11-slim

# Minimal system deps — no Chrome/Chromium needed.
# Web search now uses duckduckgo-search (pure HTTP, no browser).
# Selenium + chromium-driver are kept as optional for JS page-fetch fallback only.
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    # Shared libraries Chromium needs
    libglib2.0-0 libnss3 libnspr4 libdbus-1-3 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxcb1 libxkbcommon0 libx11-6 \
    libxcomposite1 libxdamage1 libxext6 libxfixes3 \
    libxrandr2 libgbm1 libpango-1.0-0 libcairo2 \
    libatspi2.0-0 libx11-xcb1 libxi6 libxtst6 libxrender1 \
    fonts-liberation fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Point Selenium to apt-installed chromium (version-matched with chromium-driver)
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PYTHONUNBUFFERED=1
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null
ENV SE_CACHE_PATH=/tmp/selenium

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --timeout=120 -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8501

CMD streamlit run main_ui.py \
    --server.port ${PORT:-8501} \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false
