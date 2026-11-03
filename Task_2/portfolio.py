"""Track stock holdings and append portfolio summaries to a CSV file."""

import csv
import math
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Holding:
    ticker: str
    buy_price: float
    shares: float
    current_price: float

    @property
    def invested(self) -> float:
        return self.buy_price * self.shares

    @property
    def market_value(self) -> float:
        return self.current_price * self.shares

    @property
    def gain_loss(self) -> float:
        return self.market_value - self.invested

    @property
    def gain_loss_percent(self) -> float:
        return self.gain_loss / self.invested * 100


CSV_FIELDS = [
    "timestamp",
    "ticker",
    "shares",
    "buy_price",
    "current_price",
    "invested",
    "market_value",
    "gain_loss",
    "gain_loss_percent",
    "portfolio_invested",
    "portfolio_market_value",
    "portfolio_gain_loss",
    "portfolio_gain_loss_percent",
]


def summarize_portfolio(holdings: dict[str, Holding]) -> dict[str, float]:
    invested = sum(holding.invested for holding in holdings.values())
    market_value = sum(holding.market_value for holding in holdings.values())
    gain_loss = market_value - invested
    return {
        "invested": invested,
        "market_value": market_value,
        "gain_loss": gain_loss,
        "gain_loss_percent": gain_loss / invested * 100 if invested else 0.0,
    }


def write_summary(
    holdings: dict[str, Holding], output_path: Path
) -> None:
    """Append one row per holding, including portfolio totals, to a CSV file."""
    totals = summarize_portfolio(holdings)
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    write_header = not output_path.exists() or output_path.stat().st_size == 0

    with output_path.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        if write_header:
            writer.writeheader()
        for holding in holdings.values():
            writer.writerow(
                {
                    "timestamp": timestamp,
                    "ticker": holding.ticker,
                    "shares": holding.shares,
                    "buy_price": holding.buy_price,
                    "current_price": holding.current_price,
                    "invested": holding.invested,
                    "market_value": holding.market_value,
                    "gain_loss": holding.gain_loss,
                    "gain_loss_percent": holding.gain_loss_percent,
                    "portfolio_invested": totals["invested"],
                    "portfolio_market_value": totals["market_value"],
                    "portfolio_gain_loss": totals["gain_loss"],
                    "portfolio_gain_loss_percent": totals["gain_loss_percent"],
                }
            )


def read_positive_number(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        try:
            number = float(value)
        except ValueError:
            print("Enter a valid number.")
            continue
        if not math.isfinite(number) or number <= 0:
            print("Enter a number greater than zero.")
            continue
        return number


def collect_holdings() -> dict[str, Holding]:
    holdings: dict[str, Holding] = {}
    while True:
        ticker_input = input("Ticker symbol (press Enter to finish): ").strip()
        if not ticker_input:
            break
        ticker = ticker_input.upper()
        if not re.fullmatch(r"[A-Z0-9.^-]+", ticker):
            print("Use letters, numbers, periods, hyphens, or ^ in a ticker.")
            continue
        if ticker in holdings:
            print(f"{ticker} is already in the portfolio; enter it only once.")
            continue

        buy_price = read_positive_number(f"{ticker} buy price per share: ")
        shares = read_positive_number(f"{ticker} share quantity: ")
        current_price = read_positive_number(
            f"{ticker} current price per share: "
        )
        holdings[ticker] = Holding(ticker, buy_price, shares, current_price)
    return holdings


def display_summary(holdings: dict[str, Holding]) -> None:
    print("\nPortfolio summary")
    print(
        f"{'Ticker':<10}{'Shares':>12}{'Invested':>14}{'Market value':>16}"
        f"{'Gain/loss':>14}{'Gain/loss %':>14}"
    )
    for holding in holdings.values():
        print(
            f"{holding.ticker:<10}{holding.shares:>12.4f}"
            f"{holding.invested:>14.2f}{holding.market_value:>16.2f}"
            f"{holding.gain_loss:>14.2f}{holding.gain_loss_percent:>13.2f}%"
        )

    totals = summarize_portfolio(holdings)
    print(
        f"\nTotal invested: ${totals['invested']:.2f}"
        f"\nCurrent value:  ${totals['market_value']:.2f}"
        f"\nTotal gain/loss: ${totals['gain_loss']:.2f}"
        f" ({totals['gain_loss_percent']:.2f}%)"
    )


def main() -> None:
    print("Enter a current market price for each ticker using a recent quote.")
    holdings = collect_holdings()
    if not holdings:
        print("No holdings entered; nothing to save.")
        return

    display_summary(holdings)
    output_path = Path(__file__).with_name("portfolio_summary.csv")
    write_summary(holdings, output_path)
    print(f"\nSummary appended to {output_path}")


if __name__ == "__main__":
    main()
