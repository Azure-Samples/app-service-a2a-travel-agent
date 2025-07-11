"""
Basic Semantic Kernel Travel Agent (without A2A dependencies)
This version works standalone for testing the web interface.
"""

import asyncio
import logging
from collections.abc import AsyncIterable
from typing import Any

from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class BasicTravelAgent:
    """Basic travel agent for testing without A2A/Semantic Kernel dependencies"""

    def __init__(self):
        self.sessions: dict[str, list] = {}
        logger.info("Basic Travel Agent initialized")

    async def invoke(self, user_input: str, session_id: str) -> dict[str, Any]:
        """Handle synchronous requests"""
        # Store conversation
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({"role": "user", "content": user_input})

        # Simple response logic
        response = self._generate_response(user_input)

        self.sessions[session_id].append({"role": "assistant", "content": response})

        return {"content": response, "is_task_complete": True, "require_user_input": False}

    async def stream(self, user_input: str, session_id: str) -> AsyncIterable[dict[str, Any]]:
        """Handle streaming requests"""
        # Store conversation
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({"role": "user", "content": user_input})

        # Simulate thinking
        yield {
            "content": "Let me help you with your travel request...",
            "is_task_complete": False,
            "require_user_input": False,
        }

        await asyncio.sleep(0.5)

        # Generate response
        response = self._generate_response(user_input)

        # Stream response in chunks
        words = response.split()
        chunk_size = 3
        current_text = ""

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i : i + chunk_size])
            current_text += (" " if current_text else "") + chunk

            yield {"content": current_text, "is_task_complete": False, "require_user_input": False}

            await asyncio.sleep(0.2)

        # Final response
        self.sessions[session_id].append({"role": "assistant", "content": response})

        yield {"content": response, "is_task_complete": True, "require_user_input": False}

    def _generate_response(self, user_input: str) -> str:
        """Generate a simple response based on user input"""
        user_lower = user_input.lower()

        if any(word in user_lower for word in ["currency", "exchange", "rate", "usd", "eur", "dollar"]):
            return (
                "I can help you with currency exchange rates! For real-time rates, I would normally "
                "use the Frankfurter API. For example, 1 USD is approximately 0.85 EUR today. "
                "Please note: This is a demo response. In the full version with Semantic Kernel, "
                "I would provide live exchange rates."
            )

        elif any(word in user_lower for word in ["trip", "travel", "visit", "vacation", "itinerary"]):
            return (
                "I'd love to help you plan your trip! Based on your request, I can suggest activities, "
                "accommodations, and create personalized itineraries. For a complete trip planning "
                "experience, the full Semantic Kernel version would integrate with multiple travel APIs "
                "and provide detailed recommendations based on your preferences and budget."
            )

        elif any(word in user_lower for word in ["restaurant", "food", "dining", "eat"]):
            return (
                "Great question about dining! I can recommend restaurants based on your location, "
                "cuisine preferences, and budget. The full version would integrate with restaurant "
                "APIs to provide real-time availability, reviews, and booking options."
            )

        elif any(word in user_lower for word in ["hello", "hi", "hey"]):
            return (
                "Hello! I'm your AI Travel Assistant powered by Semantic Kernel. I can help you with:\n\n"
                "• Currency exchange rates and conversions\n"
                "• Trip planning and itinerary creation\n"
                "• Activity and dining recommendations\n"
                "• Travel tips and advice\n\n"
                "What would you like help with today?"
            )

        else:
            return (
                "Thank you for your question! I'm here to help with all your travel needs. "
                "I can assist with currency exchanges, trip planning, activity recommendations, "
                "and dining suggestions. Could you please provide more specific details about "
                "what you'd like help with?"
            )


# Alias for compatibility - DISABLED: Using full Semantic Kernel version
# SemanticKernelTravelAgent = BasicTravelAgent
