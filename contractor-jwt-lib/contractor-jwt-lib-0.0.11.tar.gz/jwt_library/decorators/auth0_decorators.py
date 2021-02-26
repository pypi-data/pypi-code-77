from functools import wraps
import json
from six.moves.urllib.request import urlopen
from flask import request, _request_ctx_stack


from jwt_library.jwt_operations.auth0 import get_payload
from jwt_library.jwt_operations.auth0.jwt_operations import fetch_token_from_header, AuthError, get_unverified_header, validate_algorithm
from jose import jwt


def jwt_required_auth0(iss, aud):
    def requires_auth(f):
        """Determines if the access token is valid """
        @wraps(f)
        def decorated(*args, **kwargs):
            token = fetch_token_from_header(request.headers.get("Authorization"))
            jsonurl = urlopen("https://"+ iss +"/.well-known/jwks.json")
            jwks = json.loads(jsonurl.read())
            unverified_header = get_unverified_header(token)

            validate_algorithm(unverified_header=unverified_header)

            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
            if rsa_key:
                payload = get_payload(token=token, rsa_key=rsa_key, issuer=iss, audience=aud)
                _request_ctx_stack.top.current_user = payload
                return f(*args, **kwargs)
            raise AuthError({"status": "invalid_header",
                            "message": "Unable to find appropriate key"}, 401)
        return decorated
    return requires_auth