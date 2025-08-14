import asyncio
import aiohttp
import json
import time

class MarketDataCollector:
    def __init__(self, exchange_api_keys):
        self.exchange_api_keys = exchange_api_keys
        self.base_urls = {
            "binance": "https://api.binance.com/api/v3",
            "coinbase": "https://api.coinbase.com/v2",
            # Add other exchanges as needed
        }

    async def fetch_klines(self, exchange, symbol, interval, limit):
        url = ""
        headers = {}
        if exchange == "binance":
            url = f"{self.base_urls['binance']}/klines?symbol={symbol}&interval={interval}&limit={limit}"
        elif exchange == "coinbase":
            # Coinbase API for klines is more complex, often requires authentication and specific product_id
            # This is a simplified example, actual implementation would need more details
            print(f"Warning: Coinbase klines fetching is not fully implemented in this example.")
            return []
        else:
            print(f"Error: Unsupported exchange {exchange}")
            return []

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
                    data = await response.json()
                    return data
            except aiohttp.ClientError as e:
                print(f"Error fetching klines from {exchange}: {e}")
                return []

    async def fetch_order_book(self, exchange, symbol, limit):
        url = ""
        headers = {}
        if exchange == "binance":
            url = f"{self.base_urls['binance']}/depth?symbol={symbol}&limit={limit}"
        elif exchange == "coinbase":
            print(f"Warning: Coinbase order book fetching is not fully implemented in this example.")
            return {}
        else:
            print(f"Error: Unsupported exchange {exchange}")
            return {}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data
            except aiohttp.ClientError as e:
                print(f"Error fetching order book from {exchange}: {e}")
                return {}

    async def collect_market_data(self, exchange, symbol, kline_interval='1m', kline_limit=100, order_book_limit=100):
        print(f"Collecting market data for {symbol} on {exchange}...")
        klines = await self.fetch_klines(exchange, symbol, kline_interval, kline_limit)
        order_book = await self.fetch_order_book(exchange, symbol, order_book_limit)

        market_data = {
            "timestamp": int(time.time() * 1000), # Milliseconds
            "exchange": exchange,
            "symbol": symbol,
            "klines": klines,
            "order_book": order_book
        }
        print(f"Collected data for {symbol} on {exchange}.")
        return market_data

async def main():
    # In a real scenario, API keys would be loaded securely from environment variables or a config file
    exchange_api_keys = {
        "binance": {"api_key": "YOUR_BINANCE_API_KEY", "secret_key": "YOUR_BINANCE_SECRET_KEY"},
        "coinbase": {"api_key": "YOUR_COINBASE_API_KEY", "secret_key": "YOUR_COINBASE_SECRET_KEY"},
    }
    collector = MarketDataCollector(exchange_api_keys)

    # Example usage:
    binance_btc_data = await collector.collect_market_data("binance", "BTCUSDT", kline_interval='1m', kline_limit=5)
    print("\nBinance BTCUSDT Data:")
    print(json.dumps(binance_btc_data, indent=2))

    # You would typically send this data to a message queue or storage service
    # For example: await send_to_kafka(binance_btc_data)

if __name__ == "__main__":
    asyncio.run(main())


