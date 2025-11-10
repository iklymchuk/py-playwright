#!/bin/bash

# Test Automation Framework - Quick Setup Script

echo "=========================================="
echo "UI Test Automation Framework Setup"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | grep -oP '\d+\.\d+')
required_version="3.10"

if (( $(echo "$python_version < $required_version" | bc -l) )); then
    echo "❌ Python 3.10+ is required. Current: $python_version"
    exit 1
else
    echo "✅ Python version: $python_version"
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
else
    python -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers..."
playwright install
playwright install-deps
echo "✅ Playwright browsers installed"

# Create .env file
echo ""
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists"
else
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
fi

# Create directories
echo ""
echo "Creating required directories..."
mkdir -p artifacts/screenshots
mkdir -p artifacts/videos
mkdir -p artifacts/traces
mkdir -p artifacts/logs
mkdir -p reports/allure-results
mkdir -p reports/allure-report
echo "✅ Directories created"

# Run quick validation
echo ""
echo "Running quick validation..."
pytest tests/test_smoke.py::TestLoginSmoke::test_login_page_elements_visible -v --browser=chromium --headless=true --maxfail=1

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Setup completed successfully!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file with your configuration"
    echo "2. Run tests: pytest -m smoke"
    echo "3. View reports: allure serve reports/allure-results"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "⚠️  Setup completed with validation errors"
    echo "=========================================="
    echo "Please check the test configuration"
fi
