import logging

import httpx
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import BasePushNotificationSender, InMemoryPushNotificationConfigStore, InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from .agent_executor import SemanticKernelTravelAgentExecutor

logger = logging.getLogger(__name__)


class A2AServer:
    """A2A Server wrapper for the Semantic Kernel Travel Agent"""

    def __init__(self, httpx_client: httpx.AsyncClient, host: str = "localhost", port: int = 8000):
        self.httpx_client = httpx_client
        self.host = host
        self.port = port
        self._setup_server()

    def _setup_server(self):
        """Setup the A2A server with the travel agent"""
        # Setup A2A components
        config_store = InMemoryPushNotificationConfigStore()
        push_sender = BasePushNotificationSender(self.httpx_client, config_store)

        request_handler = DefaultRequestHandler(
            agent_executor=SemanticKernelTravelAgentExecutor(),
            task_store=InMemoryTaskStore(),
            push_config_store=config_store,
            push_sender=push_sender,
        )

        # Create A2A Starlette application
        self.a2a_app = A2AStarletteApplication(agent_card=self._get_agent_card(), http_handler=request_handler)

        logger.info(f"A2A server configured for {self.host}:{self.port}")

    def _get_agent_card(self) -> AgentCard:
        """Returns the Agent Card for the Semantic Kernel Travel Agent."""
        capabilities = AgentCapabilities(streaming=True)

        skill_trip_planning = AgentSkill(
            id="trip_planning_sk",
            name="Semantic Kernel Trip Planning",
            description=(
                "Handles comprehensive trip planning, including currency exchanges, itinerary creation, sightseeing, "
                "dining recommendations, and event bookings using Frankfurter API for currency conversions."
            ),
            tags=["trip", "planning", "travel", "currency", "semantic-kernel"],
            examples=[
                "Plan a budget-friendly day trip to Seoul including currency exchange.",
                "What's the exchange rate and recommended itinerary for visiting Tokyo?",
                "I need a 3-day itinerary for Paris with a budget of $500 USD.",
                "Convert 1000 USD to EUR and suggest affordable restaurants in Rome.",
            ],
        )

        agent_card = AgentCard(
            name="SK Travel Agent",
            description=(
                "Semantic Kernel-based travel agent providing comprehensive trip planning services "
                "including currency exchange and personalized activity planning."
            ),
            url=f"http://{self.host}:{self.port}/",
            version="1.0.0",
            defaultInputModes=["text"],
            defaultOutputModes=["text"],
            capabilities=capabilities,
            skills=[skill_trip_planning],
        )

        return agent_card

    def get_starlette_app(self):
        """Get the Starlette app for mounting in FastAPI"""
        return self.a2a_app.build()
