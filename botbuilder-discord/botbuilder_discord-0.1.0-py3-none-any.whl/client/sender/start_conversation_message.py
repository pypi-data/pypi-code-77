
from . import BaseMessage


class StartConversationMessage(BaseMessage):

    def create_request_body(self) -> dict:

        activity_id = self.options.get('activity_id')
        user_id = self.options.get('user_id')

        return {
            "type": "conversationUpdate",
            "serviceUrl": f"http://{self.listener_host}:{self.listener_port}",
            "id": activity_id,
            "from": {
                "id": f"bot_{user_id}",
            },
            "conversation": {
                "id": user_id,
            },
            "recipient": {
                "id": user_id,
            },
            "membersAdded": [
                {
                    "id": f"bot_{user_id}",
                },
                {
                    "id": user_id,
                }
            ],
            "membersRemoved": []
        }
