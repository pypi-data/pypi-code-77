from covid_cloud.client import *
from covid_cloud import constants


class COVIDCloud:
    def __init__(self, client_id='', client_secret='', personal_access_token='', search_url=None, drs_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.personal_access_token = personal_access_token
        self.search_url = search_url
        self.drs_url = drs_url
        self.oauth_token = None

    def login(self, email, personal_access_token=None, client_id=None, client_secret=None, client_redirect_uri=None,
              wallet_uri=None, search_url=None, drs_url=None):
        self.oauth_token = login(email=email,
                                 personal_access_token=self.personal_access_token,
                                 client_id=self.client_id,
                                 client_secret=self.client_secret,
                                 client_redirect_uri=constants.redirect_uri,
                                 wallet_uri=constants.wallet_uri,
                                 search_url=self.search_url,
                                 drs_url=self.drs_url)['access_token']

    def query(self, q, download=False, use_json=False, raw=False):
        return query(self.search_url, q, download, use_json, raw, self.oauth_token)

    def list_tables(self):
        return get_tables(self.search_url, self.oauth_token)

    def get_table(self, table_name):
        return get_table(self.search_url, table_name, self.oauth_token)

    def download(self, urls, output_dir=downloads_directory):
        return download_files(self.drs_url, urls, output_dir, self.oauth_token)
