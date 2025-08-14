import pandas as pd
import numpy as np
from datetime import datetime

class DataProcessor:
    def __init__(self):
        pass

    def process_market_data(self, klines, order_book):
        # Example: Convert klines to DataFrame and calculate simple moving average
        if not klines:
            return {"processed_klines": [], "order_book_summary": {}}

        df = pd.DataFrame(klines, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df["close"] = pd.to_numeric(df["close"])
        df["volume"] = pd.to_numeric(df["volume"])

        df["SMA_10"] = df["close"].rolling(window=10).mean()
        df["RSI"] = self._calculate_rsi(df["close"], window=14)

        # Summarize order book
        bids = pd.DataFrame(order_book.get("bids", []), columns=["price", "quantity"])
        asks = pd.DataFrame(order_book.get("asks", []), columns=["price", "quantity"])

        order_book_summary = {
            "total_bid_volume": bids["quantity"].sum() if not bids.empty else 0,
            "total_ask_volume": asks["quantity"].sum() if not asks.empty else 0,
            "bid_ask_spread": (asks["price"].min() - bids["price"].max()) if not asks.empty and not bids.empty else 0
        }

        return {
            "processed_klines": df.to_dict(orient="records"),
            "order_book_summary": order_book_summary
        }

    def _calculate_rsi(self, prices, window=14):
        # Simple RSI calculation for demonstration
        diff = prices.diff(1)
        gain = diff.where(diff > 0, 0)
        loss = -diff.where(diff < 0, 0)

        avg_gain = gain.ewm(com=window - 1, min_periods=window).mean()
        avg_loss = loss.ewm(com=window - 1, min_periods=window).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def process_on_chain_data(self, on_chain_data):
        # Example: Identify large transactions or new token deployments
        processed_txs = []
        for tx in on_chain_data.get("transactions", []):
            # Simple heuristic for large transactions
            if tx.get("value", 0) > 100: # Example: transactions > 100 ETH
                tx["is_large_transaction"] = True
            else:
                tx["is_large_transaction"] = False
            processed_txs.append(tx)
        
        # Placeholder for new token deployment detection
        # This would involve more complex logic, e.g., checking contract creation events
        new_token_deployments = [] 

        return {"processed_transactions": processed_txs, "new_token_deployments": new_token_deployments}

    def process_social_media_data(self, tweets):
        # Example: Sentiment analysis (placeholder) and KOL identification
        processed_tweets = []
        for tweet in tweets:
            # Placeholder for sentiment analysis
            tweet["sentiment"] = self._analyze_sentiment(tweet["text"])
            
            # Simple KOL identification based on followers count
            if tweet["user"]["followers_count"] > 100000 and tweet["user"]["verified"]:
                tweet["is_kol"] = True
            else:
                tweet["is_kol"] = False
            processed_tweets.append(tweet)
        return processed_tweets

    def _analyze_sentiment(self, text):
        # This is a very basic placeholder. In a real system, you'd use an NLP model.
        text_lower = text.lower()
        if "buy" in text_lower or "long" in text_lower or "bullish" in text_lower or "pump" in text_lower:
            return "positive"
        elif "sell" in text_lower or "short" in text_lower or "bearish" in text_lower or "dump" in text_lower:
            return "negative"
        else:
            return "neutral"

async def main():
    processor = DataProcessor()

    # Example Market Data Processing
    sample_klines = [
        [1678886400000, "20000", "20100", "19900", "20050", "100", 1678886459999, "2000000", 1000, "50", "1000000", "0"],
        [1678886460000, "20050", "20150", "19950", "20100", "120", 1678886519999, "2400000", 1200, "60", "1200000", "0"],
        [1678886520000, "20100", "20200", "20000", "20150", "150", 1678886579999, "3000000", 1500, "70", "1500000", "0"],
        [1678886580000, "20150", "20250", "20050", "20200", "130", 1678886639999, "2600000", 1300, "65", "1300000", "0"],
        [1678886640000, "20200", "20300", "20100", "20250", "110", 1678886699999, "2200000", 1100, "55", "1100000", "0"],
        [1678886700000, "20250", "20350", "20150", "20300", "140", 1678886759999, "2800000", 1400, "70", "1400000", "0"],
        [1678886760000, "20300", "20400", "20200", "20350", "160", 1678886819999, "3200000", 1600, "80", "1600000", "0"],
        [1678886820000, "20350", "20450", "20250", "20400", "170", 1678886879999, "3400000", 1700, "85", "1700000", "0"],
        [1678886880000, "20400", "20500", "20300", "20450", "180", 1678886939999, "3600000", 1800, "90", "1800000", "0"],
        [1678886940000, "20450", "20550", "20350", "20500", "190", 1678886999999, "3800000", 1900, "95", "1900000", "0"],
        [1678887000000, "20500", "20600", "20400", "20550", "200", 1678887059999, "4000000", 2000, "100", "2000000", "0"],
        [1678887060000, "20550", "20650", "20450", "20600", "210", 1678887119999, "4200000", 2100, "105", "2100000", "0"],
        [1678887120000, "20600", "20700", "20500", "20650", "220", 1678887179999, "4400000", 2200, "110", "2200000", "0"],
        [1678887180000, "20650", "20750", "20550", "20700", "230", 1678887239999, "4600000", 2300, "115", "2300000", "0"],
        [1678887240000, "20700", "20800", "20600", "20750", "240", 1678887299999, "4800000", 2400, "120", "2400000", "0"],
    ]
    sample_order_book = {"bids": [["20000", "5"], ["19990", "10"]], "asks": [["20010", "3"], ["20020", "7"]]}
    processed_market_data = processor.process_market_data(sample_klines, sample_order_book)
    print("\nProcessed Market Data:")
    print(json.dumps(processed_market_data, indent=2))

    # Example On-chain Data Processing
    sample_on_chain_data = {
        "block_number": 12345,
        "transactions": [
            {"hash": "0x123...", "from": "0xabc...", "to": "0xdef...", "value": 50, "gas_price": 10, "input": "0x", "nonce": 1},
            {"hash": "0x456...", "from": "0xghi...", "to": "0xjkl...", "value": 200, "gas_price": 20, "input": "0x", "nonce": 2},
        ]
    }
    processed_on_chain_data = processor.process_on_chain_data(sample_on_chain_data)
    print("\nProcessed On-chain Data:")
    print(json.dumps(processed_on_chain_data, indent=2))

    # Example Social Media Data Processing
    sample_tweets = [
        {"text": "$DOGE to the moon! Buy now!", "user": {"followers_count": 150000, "verified": True}},
        {"text": "Bearish on $SHIB, time to sell.", "user": {"followers_count": 5000, "verified": False}},
    ]
    processed_social_media_data = processor.process_social_media_data(sample_tweets)
    print("\nProcessed Social Media Data:")
    print(json.dumps(processed_social_media_data, indent=2))

if __name__ == "__main__":
    asyncio.run(main())


