import os

# Gunicorn configuration for Azure App Service
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
workers = 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 300
keepalive = 2
max_requests = 1000
max_requests_jitter = 50
preload_app = True
accesslog = "-"
errorlog = "-"
capture_output = True
enable_stdio_inheritance = True
