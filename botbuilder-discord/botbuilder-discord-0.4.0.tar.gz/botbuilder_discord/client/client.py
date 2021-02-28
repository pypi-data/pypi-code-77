
from .listener import Listener
from .sender import StartConversationMessage, SendTextMessage


class Client:

    def __init__(self, bot_api_url, listener_host: str = "127.0.0.1", listener_port: int = 5789):

        # Save the urls
        self.bot_api_url = bot_api_url
        self.listener_host = listener_host
        self.listener_port = listener_port

        # Launch the listener server
        self.listener = Listener(listener_host, listener_port)
        self.listener.start()

    async def start_conversation(self, user_id: int) -> str:

        return await StartConversationMessage(
            self.bot_api_url, self.listener_host, self.listener_port, {
                'user_id': user_id
            }).send()

    async def send_message(self, user_id: int, text: str) -> str:

        return await SendTextMessage(
            self.bot_api_url, self.listener_host, self.listener_port, {
                'user_id': user_id,
                'text': text
            }).send()
