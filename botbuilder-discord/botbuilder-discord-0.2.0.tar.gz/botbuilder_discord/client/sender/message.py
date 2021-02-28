
import aiohttp
from random import randrange
from botbuilder_discord.client import response_queue


class BaseMessage:

    def __init__(self, bot_api_url, listener_host, listener_port, options: dict):

        # Save urls
        self.bot_api_url = bot_api_url
        self.listener_host = listener_host
        self.listener_port = listener_port

        # Generate a random message id
        self.activity_id = str(randrange(10_000_000))

        # Create an options dict
        self.options = options
        self.options['activity_id'] = self.activity_id

        # Init an empty response property
        self.response = None

    async def send(self):

        # Bind the callback to the response queue
        response_queue.bind_to(self.get_entries)

        # Send the request to the bot
        await self.post_request(self.create_request_body())

        # Wait the response from the listener
        return await self.await_response()

    def create_request_body(self) -> dict:
        return {}

    async def post_request(self, content: dict):

        async with aiohttp.ClientSession() as session:
            async with session.post(self.bot_api_url, json=content) as response:

                # print(response.status)
                pass

    async def await_response(self):

        # Wait for the response
        while self.response is None:
            pass

        return self.response

    def get_entries(self, entries):
        content: dict = entries.get(self.activity_id, None)

        if content is not None:
            response_queue.unbind(self.get_entries)
            self.response = content.get('text', False)
