import threading
from http import HTTPStatus
from flask import Flask, request, Response
from flask.views import MethodView

from botbuilder_discord.client import response_queue


class Listener(threading.Thread):

    def __init__(self, host: str = "127.0.01", port: int = 5789):
        super().__init__()

        self.host = host
        self.port = port

        # Create Flask server
        self.app = Flask("Flask")

        # Add routes
        self.app.add_url_rule(
            '/v3/conversations/<conversation_id>/activities/<activity_id>',
            view_func=Conversation.as_view('conversation'),
            methods=['POST']
        )
        # self.app.add_url_rule('/{tail:.*}', view_func=CatchAll.as_view('catch_all'), methods=['POST'])

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=True, use_reloader=False)


class Conversation(MethodView):

    def post(self, conversation_id: str, activity_id: str):
        """
        :param conversation_id: The id of the conversation. This id is also
            the discord id of the user involved into the conversation.
        :param activity_id: The unique id of the message, created when the
            user send its message to the bot, and passed back to the listener.

        :return:
        """

        # Check if the data send is a JSON
        if "application/json" in request.headers["Content-Type"]:

            # Get the message
            body = request.json or {}
            text = body.get('text', None)

            # Set the data into the queue
            response_queue.append(activity_id, {
                'message_id': activity_id,
                'user_id': conversation_id,
                'text': text
            })

        # If no JSON is send, return "Unsupported media type"
        else:
            return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        # Return HTTP 200 OK
        return Response(status=HTTPStatus.OK)
