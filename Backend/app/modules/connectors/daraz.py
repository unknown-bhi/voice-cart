import hmac
import hashlib
import time
import httpx
from urllib.parse import urlencode

class DarazClient:
    def __init__(self, api_key :str, api_secret : str, access_token : str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token


    def _genrate_signature(self, endpoint :str, params : dict):

        sorted_params = sorted(params.items())

        query_string = urlencode(sorted_params)

        string_to_sign =f'{endpoint}{query_string}'

        signature =hmac.new(
            self.api_secret.encode('utf-8'),
            string_to_sign.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    async def get_orders(self):

        endpoint ='/order/get'
        params ={
            'app_key' : self.api_key,
            'access_token' : self.access_token,
            'timestamp' : str(int(time.time() * 1000)),
            'sign_method' : 'sha256'
        }

        signature = self._genrate_signature(endpoint, params)
        params['sign'] = signature

        # in a real scenario, we would use httpx to make the call:
        # async with httpx.AsyncClient() as client:
        #     res = await client.get(f'{self.base_url}{endpoint}',params=params)
        #     return res.json()

        return {'total_orders' : 15,
                'pending' : 2,
                'shipped' : 10,
                'delivered' : 3,
                'revenue' : '85000 pkr'
                }