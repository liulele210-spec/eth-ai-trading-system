import requests
from .config import BASE_URL, SYMBOL


class BinanceClient:

    def __init__(self):
        self.base_url = BASE_URL
        self.symbol = SYMBOL

    def _get(self, path, params=None):

        url = self.base_url + path

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    def get_price(self):

        return self._get(
            "/fapi/v1/ticker/price",
            {
                "symbol": self.symbol
            }
        )

    def get_24h_ticker(self):

        return self._get(
            "/fapi/v1/ticker/24hr",
            {
                "symbol": self.symbol
            }
        )

    def get_klines(
        self,
        interval,
        limit=200
    ):

        return self._get(
            "/fapi/v1/klines",
            {
                "symbol": self.symbol,
                "interval": interval,
                "limit": limit
            }
        )

    def get_open_interest(self):

        return self._get(
            "/fapi/v1/openInterest",
            {
                "symbol": self.symbol
            }
        )

    def get_funding_rate(self):

        return self._get(
            "/fapi/v1/fundingRate",
            {
                "symbol": self.symbol,
                "limit": 1
            }
        )

    def get_order_book(
        self,
        limit=20
    ):

        return self._get(
            "/fapi/v1/depth",
            {
                "symbol": self.symbol,
                "limit": limit
            }
        )