# Makefile for Semantic Kernel A2A Travel Agent

.PHONY: install install-dev clean lint format test run docker-build docker-run help

# Default target
.DEFAULT_GOAL := help

# Virtual environment
VENV := .venv
PYTHON := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip

# Help target
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

# Installation targets
install: ## Install production dependencies
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt

install-dev: ## Install development dependencies
	python -m venv $(VENV)
	$(PIP) install -r requirements-dev.txt

# Clean targets
clean: ## Clean up cache and temporary files
	powershell -Command "Remove-Item -Path '__pycache__', '*.pyc', '.pytest_cache', '.coverage', '.mypy_cache' -Recurse -Force -ErrorAction SilentlyContinue"
	powershell -Command "Get-ChildItem -Path . -Name '__pycache__' -Recurse | Remove-Item -Recurse -Force"

# Code quality targets
lint: ## Run linting with ruff
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

format: ## Format code with ruff
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check . --fix

# Testing targets
test: ## Run tests
	$(PYTHON) -m pytest tests/ -v

test-coverage: ## Run tests with coverage
	$(PYTHON) -m pytest tests/ --cov=src --cov-report=html --cov-report=term

# Running targets
run: ## Run the application locally
	$(PYTHON) -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

run-prod: ## Run the application in production mode
	$(PYTHON) -m uvicorn main:app --host 0.0.0.0 --port 8000

# Azure deployment targets
azure-login: ## Login to Azure
	az login
	azd auth login

azure-deploy: ## Deploy to Azure
	azd up

azure-logs: ## Show Azure logs
	azd show

# Docker targets
docker-build: ## Build Docker image
	docker build -t semantic-kernel-travel-agent .

docker-run: ## Run Docker container
	docker run -p 8000:8000 --env-file .env semantic-kernel-travel-agent

# Development targets
dev-setup: install-dev ## Complete development setup
	@echo "Development environment ready!"
	@echo "Run 'make run' to start the application"

requirements: ## Update requirements.txt from pyproject.toml
	$(PIP) install pip-tools
	$(PYTHON) -m pip-compile pyproject.toml
