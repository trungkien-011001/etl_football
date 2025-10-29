# --- Base: Apache Airflow with Python ---
FROM apache/airflow:2.9.3-python3.10
# Switch to root to install system packages
USER root

# ---- Install dependencies ----
RUN apt-get update && \
    apt-get install -y wget gnupg unzip curl && \
    rm -rf /var/lib/apt/lists/*

# ---- Install Google Chrome ----
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
      > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Match Chrome version with ChromeDriver
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d'.' -f1) && \
    LATEST_DRIVER=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE") && \
    wget -q "https://storage.googleapis.com/chrome-for-testing-public/${LATEST_DRIVER}/linux64/chromedriver-linux64.zip" && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chown airflow:root /usr/local/bin/chromedriver && \
    chmod 755 /usr/local/bin/chromedriver && \
    rm -rf chromedriver-linux64.zip chromedriver-linux64

# ---- Verify versions ----
RUN google-chrome --version && chromedriver --version

# Switch back to airflow user
USER airflow

# Set environment variables
ENV AIRFLOW_HOME=/opt/airflow

# Install Python dependencies
RUN pip install --no-cache-dir selenium==4.24.0 undetected-chromedriver==3.5.5 pandas==2.2.3 psycopg2-binary==2.9.9 webdriver-manager==4.0.2