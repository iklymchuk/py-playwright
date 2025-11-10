FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium firefox webkit
RUN playwright install-deps

# Copy framework code
COPY . .

# Create directories for artifacts and reports
RUN mkdir -p artifacts reports

# Set environment variables
ENV PYTHONPATH=/app
ENV CI=true

# Default command
CMD ["pytest", "--browser=chromium", "--headless=true", "--report=allure"]
