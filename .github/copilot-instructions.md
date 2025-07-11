<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Semantic Kernel A2A Travel Agent Project Instructions

This is a standalone web application that combines Semantic Kernel AI agents with Google's Agent-to-Agent (A2A) protocol for travel planning services.

## Key Technologies & Frameworks

- **Backend**: FastAPI with Python 3.10+
- **AI Framework**: Microsoft Semantic Kernel 
- **Protocol**: Google's Agent-to-Agent (A2A) protocol
- **Frontend**: Modern HTML/CSS/JavaScript with real-time chat
- **Deployment**: Azure App Service with Azure Developer CLI (AZD)
- **Dependencies**: See pyproject.toml for complete list

## Code Style & Patterns

- Follow Python PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Implement async/await patterns for I/O operations
- Use Pydantic models for data validation
- Follow FastAPI best practices for API design
- Maintain separation of concerns between agent logic and web interface

## Project Structure

- `src/agent/` - Semantic Kernel agent implementation and A2A integration
- `src/api/` - FastAPI REST endpoints for web interface
- `templates/` - Jinja2 HTML templates
- `static/` - CSS/JavaScript frontend assets
- `infra/` - Azure Bicep infrastructure as code
- `main.py` - FastAPI application entry point

## A2A Protocol Implementation

- Agent discovery through structured Agent Cards
- Task coordination and delegation between agents
- Streaming support for real-time responses
- Session management for conversation context
- Full compliance with A2A specification

## Semantic Kernel Integration

- ChatCompletionAgent for main travel manager
- Plugin architecture for currency and activity planning
- Function calling for external API integration (Frankfurter API)
- Response formatting with structured outputs
- Conversation history management

## Development Guidelines

- Always handle exceptions gracefully with appropriate logging
- Use environment variables for configuration (never hardcode secrets)
- Implement proper error handling for external API calls
- Follow async patterns for non-blocking operations
- Write descriptive docstrings for all public functions
- Include type hints and maintain backwards compatibility

## Azure Deployment

- Uses Azure App Service for hosting
- Application Insights for monitoring
- Environment variables for secure configuration
- Bicep templates for infrastructure as code
- AZD templates for streamlined deployment
