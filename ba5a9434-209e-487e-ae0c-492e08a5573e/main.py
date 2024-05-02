from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.asset = "SPXL"
        self.buy_threshold = -0.05  # 5% drop is -5%
        self.stop_loss_threshold = -0.15  # 15% loss
        self.entry_price = None  # To track entry price for stop loss calculation

    @property
    def assets(self):
        return [self.asset]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        ohlcv = data["ohlcv"]
        allocation = {self.asset: 0}  # Default to no allocation

        if len(ohlcv) >= 2:  # Ensure we have at least two days of data
            # Calculate the daily return
            prev_close = ohlcv[-2][self.asset]["close"]
            today_close = ohlcv[-1][self.asset]["close"]
            daily_return = (today_close - prev_close) / prev_close

            # Check if SPXL dropped by 5% or more
            if daily_return <= self.buy_threshold:
                # Buy (or maintain position if already holding)
                allocation[self.asset] = 1.0
                self.entry_price = today_close  # Update entry price
                log("Buying SPXL due to 5% drop.")

            # Calculate the loss from entry price if currently holding SPXL
            if self.entry_price is not None:
                loss_from_entry = (today_close - self.entry_price) / self.entry_price
                # Check for stop loss condition
                if loss_from_entry <= self.stop_loss_threshold:
                    allocation[self.asset] = 0  # Sell to stop loss
                    self.entry_price = None  # Reset entry price
                    log("Selling SPXL due to 15% loss from entry.")
        else:
            # Not enough data to evaluate purchase
            log("Insufficient data to evaluate SPXL for buying or selling.")

        return TargetAllocation(allocation)