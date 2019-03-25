import time

from ds_config import DSConfig

TOKEN_REPLACEMENT_IN_SECONDS = 10 * 60

class ExampleBase:
    """
    Example Base class
    """
    accountID = None
    api_client = None
    _token_received = False
    account = None
    expiresTimestamp = 0
    access_token = None

    def __init__(self, api_client):
        ExampleBase.api_client = api_client

    def check_token(self):
        current_time = int(round(time.time()))
        if not ExampleBase._token_received \
                or ((current_time + TOKEN_REPLACEMENT_IN_SECONDS) > ExampleBase.expiresTimestamp):
            self.update_token()

    def update_token(self):
        client = ExampleBase.api_client

        print ("Requesting an access token via JWT grant...", end='')
        client_id = DSConfig.client_id()
        user_id = DSConfig.impersonated_user_guid()
        aud = DSConfig.aud()
        private_key_bytes = DSConfig.private_key()
        expires_in = 3600
        oauth_results = client.request_jwt_user_token(client_id, user_id, aud, private_key_bytes, expires_in)
        
        ExampleBase.access_token = oauth_results.access_token
        if ExampleBase.account is None:
            account = self.get_account_info(client)

        ExampleBase.base_uri = account.base_uri + '/restapi'
        ExampleBase.accountID = account.account_id
        client.host = ExampleBase.base_uri
        ExampleBase._token_received = True
        ExampleBase.expiresTimestamp = (int(round(time.time())) + int(oauth_results.expires_in))
        print ("Done. Continuing...")

    def get_account_info(self, client):
        client.set_oauth_base_path(DSConfig.aud())
        response = client.get_user_info(ExampleBase.access_token)

        accounts = response.accounts
        target = DSConfig.target_account_id()

        if target is None or target == "FALSE":
            # Look for default
            for acct in accounts:
                if acct.is_default == 'True':
                    return acct

        # Look for specific account
        for acct in accounts:
            if acct.account_id == target:
                return acct

        raise Exception(f"\n\nUser does not have access to account {target}\n\n")

