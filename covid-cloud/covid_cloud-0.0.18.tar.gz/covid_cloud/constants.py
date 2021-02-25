import os

wallet_uri = 'https://wallet.staging.dnastack.com' #TODO: replace with prod
redirect_uri = "https://92a15358-9be7-4edf-8758-ec87ee1f81e3.mock.pstmn.io/" #TODO: replace this with a proper DNAstack URI

config_file_path = f"{os.path.expanduser('~')}/.covid-cloud/config.yaml"
cli_directory = f"{os.path.expanduser('~')}/.covid-cloud"
downloads_directory = f"{os.path.expanduser('~')}/.covid-cloud/downloads"

ACCEPTED_CONFIG_KEYS = ['search-url', 'drs-url', 'personal_access_token', 'email', 'oauth_token', 'oauth_token_expiry',
                        'wallet-url', 'client-id', 'client-secret', 'client-redirect-uri']
