# Semantic Kernel A2A Travel Agent

> **🔄 Adapted from Microsoft Sources**  
> This sample was adapted from the [Microsoft DevBlogs Semantic Kernel A2A Integration article](https://devblogs.microsoft.com/foundry/semantic-kernel-a2a-integration/) and the [A2A Samples repository](https://github.com/a2aproject/a2a-samples/tree/main/samples/python/agents/semantickernel) to run as a single standalone web application on Azure App Service with a modern web interface.

A standalone web application that combines Semantic Kernel AI agents with Google's Agent-to-Agent (A2A) protocol to provide comprehensive travel planning services. This application features a modern web interface and is designed for deployment on Azure App Service.

## Features

### 🤖 AI-Powered Travel Assistant
- **Currency Exchange**: Real-time exchange rates using the Frankfurter API
- **Trip Planning**: Personalized itinerary creation and recommendations
- **Activity Suggestions**: Curated local activities and attractions
- **Dining Recommendations**: Restaurant suggestions based on budget and preferences

### 🌐 Modern Web Interface
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Chat**: Interactive chat interface with typing indicators
- **Streaming Responses**: Live streaming of AI responses for better UX
- **Session Management**: Maintains conversation context across interactions

### 🔗 A2A Protocol Integration
- **Agent Discovery**: Advertises capabilities through structured Agent Cards
- **Task Coordination**: Supports multi-agent task delegation and coordination
- **Streaming Support**: Full streaming capabilities for real-time interactions
- **Protocol Compliance**: Fully compliant with Google's A2A specification

### ☁️ Azure-Ready Deployment
- **App Service Optimized**: Configured for Azure App Service deployment
- **Azure Developer CLI**: Complete AZD template for easy deployment
- **Environment Management**: Secure handling of API keys and configuration
- **Monitoring**: Application Insights integration for observability

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Browser   │───▶│   FastAPI App    │───▶│ Semantic Kernel │
│                 │    │                  │    │   Travel Agent  │
│ - Modern UI     │    │ - REST API       │    │                 │
│ - Chat Interface│    │ - A2A Protocol   │    │ - Currency API  │
│ - Responsive    │    │ - Session Mgmt   │    │ - Activity Plan │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   A2A Protocol   │
                       │                  │
                       │ - Agent Cards    │
                       │ - Task Streaming │
                       │ - Multi-Agent    │
                       └──────────────────┘
```

## Example Scenario

This implementation demonstrates a practical travel planning scenario using Semantic Kernel with A2A protocol integration:

### 🎯 **User Journey**
Imagine a user wants a budget-friendly trip plan with currency conversion:

1. **User Request**: "I am traveling to Seoul, South Korea for 2 days. I have a budget of $100 USD a day. How much is that in South Korean Won? What sort of things can I do and eat?"

2. **TravelManager Analysis**: The main agent receives the request and detects both currency and activity planning needs

3. **Multi-Agent Delegation**: 
   - **CurrencyExchangeAgent** is invoked to fetch live USD→KRW rates from Frankfurter API
   - **ActivityPlannerAgent** generates budget-friendly activity and dining recommendations

4. **Response Compilation**: The TravelManager combines results from both specialized agents

5. **Structured Output**: User receives a complete response with:
   - Current exchange rate ($100 USD = ~130,000 KRW)
   - Daily budget breakdown in Korean Won
   - Recommended activities within budget
   - Restaurant suggestions with price ranges

### 🔄 **Integration Flow**
![Semantic Kernel + A2A Integration](https://devblogs.microsoft.com/foundry/wp-content/uploads/sites/89/2025/04/1_mermaid_a2a.png)

*Source: [Microsoft DevBlogs - Semantic Kernel A2A Integration](https://devblogs.microsoft.com/foundry/semantic-kernel-a2a-integration/)*

### 🤝 **A2A Protocol Benefits**
- **Agent Discovery**: Other A2A agents can discover and delegate travel tasks to your agent
- **Task Coordination**: Seamless handoffs between specialized agents across different platforms
- **Streaming Support**: Real-time progress updates during complex multi-agent workflows
- **Cross-Cloud Compatibility**: Works with any A2A-compliant agent regardless of hosting platform

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Azure CLI (for deployment)
- Azure Developer CLI (azd)
- OpenAI or Azure OpenAI API access

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd semantic-kernel-travel-agent
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Authenticate with Azure** (for Azure OpenAI without API key):
   ```bash
   az login
   ```

4. **Run the application**:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Open your browser** to `http://localhost:8000`

### Azure Deployment

**✅ Ready to Deploy**: This application includes a complete Azure Developer CLI (AZD) template for one-command deployment.

1. **Authenticate with Azure Developer CLI**:
    ```bash
    azd auth login
    ```

2. **Initialize and deploy**:
   ```bash
   azd up
   ```

3. **Configure API key** (optional for local development):
   - For **Azure deployment**: Authentication uses managed identity automatically (no manual configuration needed)
   - For **local development**: Optionally add `AZURE_OPENAI_API_KEY` to your local `.env` file
   - If no API key is provided locally, Azure CLI credentials will be used for authentication

4. **Access your deployed application**:
   - The AZD template will output your application URL
   - Example: `https://appweb-xxxxxxxxx.azurewebsites.net`

**What gets deployed**:
- ✅ Azure App Service Plan (P0V3 for production readiness)
- ✅ Azure App Service with Python 3.11 runtime and managed identity
- ✅ Azure OpenAI resource with `gpt-4.1-mini` model
- ✅ Role assignment for secure managed identity authentication
- ✅ All necessary environment variables pre-configured
- ✅ Automatic build and deployment from source code

## Implementation Details

### 🧠 Semantic Kernel Multi-Agent Architecture

The application uses a sophisticated multi-agent architecture powered by Semantic Kernel:

- **TravelManagerAgent**: Main orchestrator that analyzes requests and delegates to specialized agents
- **CurrencyExchangeAgent**: Handles all currency-related queries with live Frankfurter API integration
- **ActivityPlannerAgent**: Creates detailed travel itineraries and activity recommendations

### 🔄 **How A2A Integration Works**

- **Task Routing and Delegation**: The TravelManager dynamically routes tasks to specialized agents, which are configured as plugins within the TravelManager itself. Leveraging context awareness and automatic function calling, the underlying model intelligently determines the most suitable agent to handle each request.

- **Agent Discovery**: Agents advertise their capabilities through a structured "Agent Card," enabling client agents to efficiently identify and select the most suitable agent for a given task, facilitating seamless communication through the A2A protocol.

- **Conversational Memory**: Semantic Kernel maintains context using its chat history across multi-turn interactions, providing a seamless user experience. Session history is maintained throughout the conversation flow.

### 🔧 Technical Stack

- **Framework**: FastAPI with async/await support
- **AI Engine**: Microsoft Semantic Kernel with Azure OpenAI/OpenAI integration
- **Protocol**: Google's Agent-to-Agent (A2A) for multi-agent coordination
- **Database**: SQLite with A2A SDK for task persistence
- **Frontend**: Modern HTML5/CSS3/JavaScript with real-time chat
- **Deployment**: Azure App Service with Bicep infrastructure as code

### 🌟 Key Features

- **Real-time Currency Conversion**: Live exchange rates via Frankfurter API
- **Function Calling**: Semantic Kernel plugins for external API integration
- **Streaming Responses**: Progressive response delivery for better UX
- **Session Management**: Persistent conversation history across interactions
- **Error Handling**: Graceful degradation with comprehensive error recovery

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI service endpoint | Yes (if using Azure OpenAI) |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | No (uses managed identity in Azure, optional for local dev) |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Azure OpenAI deployment name | Yes (if using Azure OpenAI) |
| `AZURE_OPENAI_API_VERSION` | Azure OpenAI API version | Yes (if using Azure OpenAI) |
| `OPENAI_API_KEY` | OpenAI API key | Yes (if using OpenAI) |
| `OPENAI_MODEL_ID` | OpenAI model ID (e.g., gpt-4) | Yes (if using OpenAI) |
| `HOST` | Application host (default: 0.0.0.0) | No |
| `PORT` | Application port (default: 8000) | No |
| `DEBUG` | Enable debug mode (default: false) | No |

### Authentication

This application uses **managed identity authentication** for Azure OpenAI when deployed to Azure, providing enhanced security without the need to manage API keys.

**Authentication Methods**:
- **Azure Deployment**: Uses system-assigned managed identity with automatic role assignment to "Cognitive Services OpenAI User"
- **Local Development**: 
  - Option 1: Use Azure CLI credentials (`az login`) for keyless authentication
  - Option 2: Set `AZURE_OPENAI_API_KEY` in your local `.env` file for traditional API key authentication

**For Azure OpenAI**:
- Ensure your Azure OpenAI resource has the `gpt-4.1-mini` model deployed
- API version `2025-01-01-preview` is recommended for latest features
- The deployment automatically configures the necessary role assignments

### Switching Between OpenAI Services

To use **OpenAI** instead of Azure OpenAI, modify `src/agent/travel_agent.py`:

```python
# Change this line:
chat_service = get_chat_completion_service(ChatServices.AZURE_OPENAI)

# To this:
chat_service = get_chat_completion_service(ChatServices.OPENAI)
```

## API Endpoints

### Web Interface
- `GET /` - Main chat interface
- `GET /health` - Health check endpoint

### Chat API
- `POST /chat/message` - Send a message to the agent
- `POST /chat/stream` - Stream a conversation with the agent
- `GET /chat/sessions` - Get active chat sessions
- `DELETE /chat/sessions/{session_id}` - Clear a chat session

### A2A Protocol
- `GET /a2a/` - Agent discovery and capabilities
- `POST /a2a/tasks/send` - Send tasks to the agent
- `POST /a2a/tasks/stream` - Stream tasks with real-time updates

## Project Structure

```
semantic-kernel-travel-agent/
├── src/
│   ├── agent/                  # Semantic Kernel agent implementation
│   │   ├── travel_agent.py     # Full Semantic Kernel travel agent
│   │   ├── agent_executor.py   # A2A protocol executor
│   │   └── a2a_server.py       # A2A server integration
│   └── api/
│       └── chat.py             # REST API endpoints
├── templates/
│   └── index.html              # Modern web interface
├── static/
│   ├── css/style.css           # Modern CSS styling
│   └── js/chat.js              # Interactive chat functionality
├── infra/                      # Azure infrastructure (Bicep)
├── main.py                     # FastAPI application entry point
├── azure.yaml                  # Azure Developer CLI configuration
├── pyproject.toml              # Python project configuration
└── .env                        # Environment configuration
```

## Development

### Running the Application Locally
```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Start the server with hot reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing the Agent
Try these example queries in the web interface:

1. **Currency Conversion**: "What's the current USD to EUR exchange rate?"
2. **Trip Planning**: "Plan a 3-day budget trip to Tokyo with $200/day"
3. **Multi-agent Query**: "I have 500 USD budget for Seoul - convert to KRW and suggest activities"
4. **Restaurant Recommendations**: "Find affordable restaurants in Paris near the Eiffel Tower"

## A2A Protocol Integration

This application fully implements Google's Agent-to-Agent protocol:

- **Agent Discovery**: Publishes structured Agent Cards describing capabilities
- **Task Coordination**: Supports complex multi-agent workflows
- **Streaming**: Real-time streaming of responses and intermediate results
- **Session Management**: Maintains context across multi-turn conversations

### Agent Card Example

```json
{
  "name": "SK Travel Agent",
  "description": "Semantic Kernel-based travel agent...",
  "capabilities": {
    "streaming": true
  },
  "skills": [
    {
      "id": "trip_planning_sk",
      "name": "Semantic Kernel Trip Planning",
      "description": "Handles comprehensive trip planning...",
      "tags": ["trip", "planning", "travel", "currency"]
    }
  ]
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions and support:
- Create an issue in the repository
- Check the [Semantic Kernel documentation](https://learn.microsoft.com/en-us/semantic-kernel/)
- Review the [A2A protocol specification](https://google.github.io/A2A/)

---

**Built with ❤️ using Semantic Kernel, FastAPI, and Azure**
