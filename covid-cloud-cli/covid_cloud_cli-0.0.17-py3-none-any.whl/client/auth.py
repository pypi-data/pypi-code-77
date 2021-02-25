import requests as req
from urllib.parse import parse_qs
from covid_cloud.constants import *


def login(email, personal_access_token, client_id, client_secret, client_redirect_uri, wallet_uri=wallet_uri,
          search_url='', drs_url=''):
    session = req.Session()

    # login at /login/token
    session.get(f'{wallet_uri}/login/token',
                params={
                    'token': personal_access_token,
                    "email": email,
                },
                allow_redirects=False
                )

    auth_code_res = session.get(f'{wallet_uri}/oauth/authorize',
                                params={
                                    'response_type': 'code',
                                    'client_id': client_id,
                                    'redirect_uri': client_redirect_uri,
                                    'scopes': 'openid,drs-object:write,drs-object:access',
                                    'resource': f'{drs_url},{search_url}'
                                },
                                allow_redirects=False)

    auth_code = parse_qs(req.utils.urlparse(auth_code_res.headers['Location']).query)['code'][0]

    auth_token_res = session.post(f'{wallet_uri}/oauth/token',
                                  data={
                                      'grant_type': 'authorization_code',
                                      'code': auth_code,
                                      'client_id': client_id,
                                      'client_secret': client_secret
                                  }
                                  )

    json_res = auth_token_res.json()

    return json_res
