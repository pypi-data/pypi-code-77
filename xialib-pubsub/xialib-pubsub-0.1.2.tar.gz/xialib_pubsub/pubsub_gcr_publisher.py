import os
import base64
import datetime
from functools import lru_cache, wraps
import requests
import google.auth
import google.oauth2.id_token
import google.auth.transport.requests
from xialib.publisher import Publisher

token_lifetime = int(os.environ.get("GCP_TOKEN_LIFETIME", 3500))

def timed_lru_cache(maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = datetime.timedelta(seconds=token_lifetime)
        func.expiration = datetime.datetime.utcnow() + func.lifetime
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)
        return wrapped_func
    return wrapper_cache

class PubsubGcrPublisher(Publisher):
    """Google Push to Cloud Run without passing by Pubsub

    """
    blob_support = True

    @classmethod
    @timed_lru_cache()
    def get_auth_token(cls, target_audience: str) -> str:
        """ Get Auth Token for requested cloud run instance

        """
        credentials, project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        access_token = google.oauth2.id_token.fetch_id_token(auth_req, target_audience)
        return ' '.join(['Bearer', access_token])

    def check_destination(self, project_id: str, topic_id: str):
        """ Check if it is possible to publish to the specified cloud run end point

        Notes:
            We will try to get the welcome message to check the available by using the return http code.
        """
        target_audience = "https://" + topic_id
        headers = {"Authorization": self.get_auth_token(target_audience)}
        resp = requests.get(target_audience, headers=headers)
        if resp.status_code == 200:
            return True
        else:
            return False

    def _send(self, project_id: str, topic_id: str, header: dict, data):
        try:
            data = data.encode()
        except (UnicodeEncodeError, AttributeError):
            pass
        envelope = {"message": {"attributes": header, "data": base64.b64encode(data).decode()}}
        target_audience = "https://" + topic_id
        headers = {"Authorization": self.get_auth_token(target_audience)}

        resp = requests.post(target_audience, headers=headers, json=envelope)
        if resp.status_code in [200, 204]:
            self.logger.info("Sent to {}-{}: {}".format(project_id, topic_id, header))
            return "OK"
        else:
            self.logger.error("Sent failed {}-{}: {}".format(project_id, topic_id, resp.content.decode()))
