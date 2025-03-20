import os
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pycoingecko import CoinGeckoAPI

# ✅ Set up CoinGecko API
cg = CoinGeckoAPI()

# ✅ Fetch financial market data
def fetch_market_data():
    """Fetch real-time market data from Yahoo Finance and CoinGecko."""
    try:
        # Stock & Forex Data (Yahoo Finance)
        market_data = {
            "JSE All Share": yf.Ticker("^J203.JO").history(period="1d")["Close"].iloc[-1],
            "Rand / Dollar": yf.Ticker("USDZAR=X").history(period="1d")["Close"].iloc[-1],
            "Rand / Euro": yf.Ticker("EURZAR=X").history(period="1d")["Close"].iloc[-1],
            "Rand / GBP": yf.Ticker("GBPZAR=X").history(period="1d")["Close"].iloc[-1],
            "Brent ($/barrel)": yf.Ticker("BZ=F").history(period="1d")["Close"].iloc[-1],
            "Gold ($/oz)": yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1],
            "S&P 500": yf.Ticker("^GSPC").history(period="1d")["Close"].iloc[-1],
        }

        # Crypto Data (CoinGecko)
        btc_zar = cg.get_price(ids="bitcoin", vs_currencies="zar")["bitcoin"]["zar"]
        market_data["Rand / Bitcoin"] = btc_zar

        return market_data

    except Exception as e:
        print(f"❌ ERROR: Failed to fetch market data: {e}")
        return None

# ✅ Generate Financial Infographic
def generate_infographic(market_data):
    """Create a financial market infographic."""
    df = pd.DataFrame(list(market_data.items()), columns=["Category", "Price"])

    # Ensure numeric values for visualization
    df_numeric = df[df["Category"] != "Date"]

    # Set up visualization
    colors = sns.color_palette("coolwarm", len(df_numeric))
    sns.set_theme(style="whitegrid")

    # Create the infographic
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Price", y="Category", data=df_numeric, palette=colors)

    # Labels & Title
    plt.xlabel("Price / Index Value")
    plt.ylabel("Market Categories")
    plt.title("📊 Daily Market Report", fontsize=14, fontweight="bold")

    # Save infographic
    infographic_path = "financial_infographic.png"
    plt.savefig(infographic_path, dpi=300, bbox_inches="tight")

    print(f"✅ Infographic saved as: {infographic_path}")
    return infographic_path

# ✅ Main Execution
if __name__ == "__main__":
    market_data = fetch_market_data()
    if market_data:
        generate_infographic(market_data)
