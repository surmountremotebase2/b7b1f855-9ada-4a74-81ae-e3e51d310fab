from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.target_investment = 3000  # Target investment amount in USD
        self.drop_threshold = 0.05  # 5% drop
        self.stop_loss_threshold = 0.85  # 15% stop loss
        self.target_asset = "SPXL"
        self.purchase_price = None
    
    @property
    def assets(self):
        return [self.target_asset]

    @property
    def interval(self):
        return "1day"  # Daily checks

    def run(self, data):
        ohlcv_data = data["ohlcv"][-2:]  # Get the last two days of price data
        
        if len(ohlcv_data) < 2:
            return TargetAllocation({self.target_asset: 0})  # Not enough data
        
        prev_close = ohlcv_data[0][self.target_asset]["close"]
        curr_close = ohlcv_data[1][self.target_asset]["close"]

        # Check for a 5% drop in the asset's price
        if curr_close / prev_close < 1 - self.drop_threshold:
            self.purchase_price = curr_close
            allocation = self.calculate_allocation(curr_close)
            return TargetAllocation({self.target_asset: allocation})
        else:
            if self.purchase_price:
                # Implement Stop Loss - If the current price drops below 85% of the purchase price
                if curr_close < self.purchase_price * self.stop_loss_threshold:
                    log("Stop Loss Triggered - Selling SPXL")
                    return TargetAllocation({self.target_asset: 0})  # Exit position
            # No action if conditions are not met
            return TargetAllocation({self.target_asset: 0})

    def calculate_allocation(self, current_price):
        """
        Calculate the allocation for the target_asset based on the target investment
        amount and current price. This function needs the current price to calculate
        the number of shares and then calculates what fraction of the portfolio those
        shares would represent. It's a simplified representation that would need adjustment
        based on your actual portfolio size and margin considerations.
        """
        # Assuming 1 represents 100% of the cash available for this trade
        # So this calculation is a placeholder that needs proper implementation
        # based on your account management and order execution methods.
        num_shares = self.target_investment / current_price
        return num_shares  # This should be adjusted to match the platform's way to calculate allocation based on shares.