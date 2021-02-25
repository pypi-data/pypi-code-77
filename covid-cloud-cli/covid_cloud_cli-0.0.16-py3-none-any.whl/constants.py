import os

wallet_uri = 'https://wallet.prod.dnastack.com'

config_file_path = f"{os.path.expanduser('~')}/.covid-cloud/config.yaml"
cli_directory = f"{os.path.expanduser('~')}/.covid-cloud"
downloads_directory = f"{os.path.expanduser('~')}/.covid-cloud/downloads"

ACCEPTED_CONFIG_KEYS = ['search-url', 'drs-url', 'personal_access_token', 'email', 'oauth_token', 'oauth_token_expiry',
                        'wallet-url', 'client-id', 'client-secret', 'client-redirect-uri']
