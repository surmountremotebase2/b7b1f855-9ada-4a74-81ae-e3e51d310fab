from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import Asset, OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPXL"]
        self.buy_threshold = -0.02  # Target drop of more than 2%
        self.sell_threshold = 0.20  # Target gain of 20%
        self.entry_price = None  # To keep track of the buying price
        self.investment_amount = 5000  # Fixed investment amount
        self.position_size = 0  # To track the size of our position

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return [OHLCV(i) for i in self.tickers]

    def run(self, data):
        # Check if SPXL data is available
        if "SPXL" not in data["ohlcv"] or len(data["ohlcv"]["SPXL"]) < 2:
            log("Insufficient data for SPXL.")
            return TargetAllocation({})

        # Get the last two days of data
        today = data["ohlcv"]["SPXL"][-1]
        yesterday = data["ohlcv"]["SPXL"][-2]

        # Calculate the daily return
        daily_return = (today["close"] - yesterday["close"]) / yesterday["close"]

        # Strategy Logic
        if self.entry_price is not None:
            # If currently holding SPXL, check for sell condition
            current_gain = (today["close"] - self.entry_price) / self.entry_price
            if current_gain > self.sell_threshold:
                log(f"Selling SPXL, achieved {current_gain*100}% gain.")
                self.position_size = 0  # Reset position size upon selling
                self.entry_price = None  # Reset entry price
                return TargetAllocation({"SPXL": 0})

        else:
            # If not holding SPXL, check for buy condition
            if daily_return < self.buy_threshold:
                self.entry_price = today["close"]
                # Calculate the position size based on fixed investment amount and today's closing price
                self.position_size = self.investment_amount / today["close"]
                log(f"Buying SPXL, dropped by {daily_return*100}%.")
                return TargetAllocation({"SPXL": self.position_size / today["close"]})  # Normalize position size to allocation value

        # Default action if no buy or sell condition is met
        return TargetAllocation({"SPXL": self.position_size / today["close"]} if self.position_size else {})