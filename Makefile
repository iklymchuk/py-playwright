# Makefile for UI Test Automation Framework

.PHONY: help install setup clean test smoke regression e2e mobile report docker-build docker-run

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install --upgrade pip
	pip install -r requirements.txt
	playwright install

setup: install ## Complete setup including browsers
	playwright install-deps
	cp -n .env.example .env || true
	mkdir -p artifacts/{screenshots,videos,traces,logs}
	mkdir -p reports/{allure-results,allure-report}

clean: ## Clean generated files and directories
	rm -rf artifacts/* reports/* .pytest_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

test: ## Run all tests
	pytest -v

smoke: ## Run smoke tests
	pytest -m smoke -v

regression: ## Run regression tests  
	pytest -m regression -v --parallel=4 -n 4

e2e: ## Run end-to-end tests
	pytest -m e2e -v

mobile: ## Run mobile tests
	pytest -m mobile -v --device=iPhone_13

chromium: ## Run tests on Chromium
	pytest --browser=chromium -v

firefox: ## Run tests on Firefox
	pytest --browser=firefox -v

webkit: ## Run tests on WebKit
	pytest --browser=webkit -v

all-browsers: ## Run tests on all browsers
	pytest --browser=chromium -m smoke
	pytest --browser=firefox -m smoke
	pytest --browser=webkit -m smoke

parallel: ## Run tests in parallel
	pytest -n 4 -v

headless: ## Run tests in headless mode
	pytest --headless=true -v

headed: ## Run tests in headed mode
	pytest --headless=false -v

report: ## Generate and open Allure report
	allure generate reports/allure-results -o reports/allure-report --clean
	allure open reports/allure-report

report-html: ## Open HTML report
	open reports/report.html

docker-build: ## Build Docker image
	docker build -t ui-automation-framework .

docker-run: ## Run tests in Docker
	docker run --rm \
		-v $(PWD)/artifacts:/app/artifacts \
		-v $(PWD)/reports:/app/reports \
		ui-automation-framework

docker-smoke: ## Run smoke tests in Docker
	docker-compose up test-chromium

docker-all: ## Run all browser tests in Docker
	docker-compose up test-chromium test-firefox test-webkit

docker-mobile: ## Run mobile tests in Docker
	docker-compose up test-mobile

docker-clean: ## Clean Docker containers and volumes
	docker-compose down -v

lint: ## Run code linters
	black --check .
	ruff check .

format: ## Format code
	black .
	ruff check --fix .

type-check: ## Run type checking
	mypy .

ci-test: ## Run CI tests (smoke + regression)
	pytest -m "smoke or regression" -v --parallel=4 -n 4

logs: ## View structured logs
	cat artifacts/logs/test_execution_*.jsonl | jq

debug: ## Run tests with debugging
	PWDEBUG=1 pytest tests/ -v --headless=false

trace: ## Show Playwright trace
	playwright show-trace artifacts/traces/*.zip
