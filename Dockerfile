# Step 1: Use the official Python image as the base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install dependencies for Chromium and ChromeDriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    fonts-liberation \
    xdg-utils \
    chromium \
    chromium-driver \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Step 4: Copy the Python code to the container
COPY . .

# Step 5: Install Python dependencies
RUN pip install -r requirements.txt

# Step 6: Run your scraper
CMD ["python", "scraper.py"]
