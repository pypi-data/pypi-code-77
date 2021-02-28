
from . import BaseMessage


class SendTextMessage(BaseMessage):

    def create_request_body(self) -> dict:

        activity_id = self.options.get('activity_id')
        user_id = self.options.get('user_id')
        text = self.options.get('text')

        return {
            "type": "message",
            "serviceUrl": f"http://{self.listener_host}:{self.listener_port}",
            "id": activity_id,
            "channelId": "offline",
            "text": text,
            "textFormat": "plain",
            "from": {
                "id": f"bot_{user_id}",
            },
            "conversation": {
                "id": user_id,
            },
            "recipient": {
                "id": user_id,
            }
        }
