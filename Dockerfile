# Use Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install Python dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install Chromium and ChromeDriver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    gnupg \
    curl \
    unzip \
    && apt-get clean

# Install WebDriver Manager to handle Chromedriver installation automatically
RUN pip install webdriver-manager

# Set environment variables for Chrome and Chromedriver paths
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver

# Start the application
CMD ["python", "scrape.py"]