import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.agent.a2a_server import A2AServer
from src.api.chat import router as chat_router
from src.api.test_auth import router as test_auth_router

# Load environment variables
load_dotenv()

# Configure logging
log_level = logging.DEBUG if os.getenv("DEBUG", "false").lower() == "true" else logging.INFO
logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Global variables for cleanup
httpx_client: httpx.AsyncClient = None
a2a_server: A2AServer = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    global httpx_client, a2a_server

    # Startup
    logger.info("Starting Semantic Kernel Travel Agent with A2A integration...")
    httpx_client = httpx.AsyncClient(timeout=30)

    # Initialize A2A server
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    a2a_server = A2AServer(httpx_client, host=host, port=port)

    # Mount A2A endpoints to the main app
    app.mount("/a2a", a2a_server.get_starlette_app(), name="a2a")

    logger.info(f"A2A server mounted at /a2a - Agent Card available at http://{host}:{port}/a2a/")

    yield

    # Shutdown
    logger.info("Shutting down Semantic Kernel Travel Agent...")
    if httpx_client:
        await httpx_client.aclose()


# Create FastAPI app with production settings
app = FastAPI(
    title="Semantic Kernel Travel Agent",
    description="Production-ready Semantic Kernel A2A Travel Agent",
    version="1.0.0",
    docs_url="/docs" if os.getenv("DEBUG", "false").lower() == "true" else None,
    redoc_url="/redoc" if os.getenv("DEBUG", "false").lower() == "true" else None,
    lifespan=lifespan,
)

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Setup templates
templates_path = Path(__file__).parent / "templates"
templates = Jinja2Templates(directory=templates_path)

# Include API routes
app.include_router(chat_router, prefix="/api")
app.include_router(test_auth_router, prefix="/api")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main chat interface"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint for Azure App Service"""
    return {"status": "healthy", "service": "semantic-kernel-travel-agent"}


@app.get("/agent-card")
async def get_agent_card():
    """Expose the A2A Agent Card for discovery"""
    if a2a_server:
        return a2a_server._get_agent_card()
    return {"error": "A2A server not initialized"}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    uvicorn.run(app, host=host, port=port, reload=debug)
