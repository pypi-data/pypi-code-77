
from typing import List
from .client import Client


class OfflineConnector:

    def __init__(self, bot_api_url: str = "http://127.0.0.1:3978/api/messages", listener_port: int = 5789):
        self.client = Client(bot_api_url, listener_port=listener_port)

        self.has_started = []

    async def send_message(self, user_id: int, text: str) -> List[str]:

        # List to store the responses from the bot
        responses = []

        # If the user is speaking for the first time, create a conversation
        if user_id not in self.has_started:
            responses.append(await self.client.start_conversation(user_id))
            self.has_started.append(user_id)

        # Send its message to the bot
        responses.append(await self.client.send_message(user_id, text))

        return responses
