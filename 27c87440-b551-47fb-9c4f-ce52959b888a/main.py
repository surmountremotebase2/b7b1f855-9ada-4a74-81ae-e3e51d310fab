from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD, RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"  # choosing Apple Inc. for this strategy

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"  # daily data is used for this strategy

    def run(self, data):
        macd_data = MACD(self.ticker, data["ohlcv"], fast=12, slow=26)
        rsi_data = RSI(self.ticker, data["ohlcv"], length=14)
        
        allocation_dict = {self.ticker: 0}  # default to no allocation
        
        if len(macd_data["MACD"]) > 0 and len(rsi_data) > 0:
            macd_line = macd_data["MACD"][-1]  # most recent MACD value
            signal_line = macd_data["signal"][-1]  # most recent signal line value
            rsi_latest = rsi_data[-1]  # most recent RSI value

            # Buy signal: MACD crosses above signal line and RSI is above 50
            if macd_line > signal_line and rsi_latest > 50:
                allocation_dict[self.ticker] = 1  # full allocation to AAPL
                log("Buying signal detected based on MACD and RSI criteria.")
            
            # Sell signals: MACD crosses below signal line or RSI goes below 50
            elif macd_line < signal_line or rsi_latest < 50:
                allocation_dict[self.ticker] = 0  # no allocation to AAPL
                log("Selling/No buying signal detected based on MACD and RSI criteria.")

        return TargetAllocation(allocation_dict)