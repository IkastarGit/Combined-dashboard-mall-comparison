FROM python:3.11-slim

# Install ALL libraries Chromium needs on Debian Bookworm
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Chromium and its driver
    chromium \
    chromium-driver \
    # Required system libraries for Chromium to launch
    libnss3 \
    libglib2.0-0 \
    libfontconfig1 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libxrandr2 \
    libxcb1 \
    libxkbcommon0 \
    libgtk-3-0 \
    libgbm1 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxshmfence1 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    fonts-liberation \
    # Needed to avoid "No usable sandbox" on some setups
    procps \
    && rm -rf /var/lib/apt/lists/*

# Tell Chrome/Selenium where the binary is
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
# Prevent Python output buffering
ENV PYTHONUNBUFFERED=1
# Prevent dbus errors in headless Chrome
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Quick sanity check: verify chromium can print its version
RUN chromium --version && chromedriver --version

EXPOSE 8501

CMD streamlit run railway_app.py \
    --server.port ${PORT:-8501} \
    --server.address 0.0.0.0 \
    --server.headless true \
    --browser.gatherUsageStats false
