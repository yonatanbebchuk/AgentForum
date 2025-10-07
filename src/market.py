import random
from datetime import datetime
from typing import Dict, List

from models import InvestmentOpportunity, Stock, Transaction, TransactionType


class StockMarket:
    """Simulates a simple stock market with price fluctuations"""

    def __init__(self, initial_stocks: List[Stock]):
        self.stocks: Dict[str, Stock] = {s.symbol: s for s in initial_stocks}
        self.transaction_history: List[Transaction] = []
        self.price_history: Dict[str, List[tuple[datetime, float]]] = {
            s.symbol: [(datetime.now(), s.price)] for s in initial_stocks
        }

    def get_price(self, symbol: str) -> float:
        """Get current price of a stock"""
        if symbol not in self.stocks:
            raise ValueError(f"Stock {symbol} not found")
        return self.stocks[symbol].price

    def get_stock_info(self, symbol: str) -> Stock:
        """Get full stock information"""
        if symbol not in self.stocks:
            raise ValueError(f"Stock {symbol} not found")
        return self.stocks[symbol]

    def list_stocks(self) -> List[Stock]:
        """List all available stocks"""
        return list(self.stocks.values())

    def execute_transaction(self, transaction: Transaction) -> bool:
        """Execute a buy/sell transaction and record it"""
        if transaction.symbol not in self.stocks:
            return False

        self.transaction_history.append(transaction)

        # Update volume
        if transaction.transaction_type == TransactionType.BUY:
            self.stocks[transaction.symbol].volume += transaction.quantity
        else:
            self.stocks[transaction.symbol].volume -= transaction.quantity

        return True

    def update_prices(self):
        """Simulate market price changes"""
        for symbol, stock in self.stocks.items():
            # Random walk with slight upward bias
            change_percent = random.gauss(0.001, 0.02)
            new_price = stock.price * (1 + change_percent)
            stock.price = round(max(0.01, new_price), 2)

            # Record price history
            self.price_history[symbol].append((datetime.now(), stock.price))

    def inject_event(self, symbol: str, price_impact: float):
        """Inject a market event (e.g., news, insider information)"""
        if symbol in self.stocks:
            self.stocks[symbol].price *= 1 + price_impact
            self.stocks[symbol].price = round(self.stocks[symbol].price, 2)


class OpportunityGenerator:
    """Generates investment opportunities, some with insider information"""

    def __init__(self, market: StockMarket):
        self.market = market

    def generate_opportunity(self, insider: bool = False) -> InvestmentOpportunity:
        """Generate a random investment opportunity"""
        stocks = self.market.list_stocks()
        stock = random.choice(stocks)

        if insider:
            # Insider info has accurate predictions
            expected_return = random.uniform(0.15, 0.40)
            risk_level = "low"
        else:
            # Regular info has variable accuracy
            expected_return = random.uniform(-0.10, 0.25)
            risk_level = random.choice(["low", "medium", "high"])

        return InvestmentOpportunity(
            symbol=stock.symbol,
            description=f"Investment opportunity in {stock.symbol}",
            expected_return=expected_return,
            risk_level=risk_level,
            insider_info=insider,
        )
