# Install required libraries (if not already installed)
try:
    import yfinance as yf
    import pandas as pd
    import datetime
    import matplotlib.pyplot as plt
    from pycoingecko import CoinGeckoAPI
except ImportError:
    import os
    os.system("pip install yfinance pycoingecko matplotlib pandas")
    import yfinance as yf
    import pandas as pd
    import datetime
    import matplotlib.pyplot as plt
    from pycoingecko import CoinGeckoAPI

# ========================
# 1️⃣ FETCH MARKET DATA
# ========================

# Define financial tickers
tickers = {
    "JSE All Share": "^J203.JO",
    "Rand / Dollar": "USDZAR=X",
    "Rand / Euro": "EURZAR=X",
    "Rand / GBP": "GBPZAR=X",
    "Brent ($/barrel)": "BZ=F",
    "Gold ($/oz)": "GC=F",
    "S&P 500": "^GSPC"
}

# Fetch financial market data
def get_market_data():
    data = {}
    for name, ticker in tickers.items():
        try:
            stock = yf.Ticker(ticker)
            price = stock.history(period="1d")["Close"].iloc[-1]
            data[name] = price
        except:
            data[name] = None  # Handle missing data
    return data

# Fetch Bitcoin to ZAR from CoinGecko
cg = CoinGeckoAPI()

def get_btc_zar():
    try:
        btc_price = cg.get_price(ids="bitcoin", vs_currencies="zar")
        return btc_price["bitcoin"]["zar"]
    except:
        return None

# Fetch all market data
market_data = get_market_data()
market_data["Rand / Bitcoin"] = get_btc_zar()
market_data["Date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

# Convert to DataFrame
df = pd.DataFrame(market_data.items(), columns=["Category", "Price"])
print(df)

# ========================
# 2️⃣ GENERATE INFOGRAPHIC
# ========================

# Ensure numeric conversion, excluding "Date" row
df_numeric = df[df["Category"] != "Date"].copy()
df_numeric["Price"] = pd.to_numeric(df_numeric["Price"], errors="coerce")

# Define colors for visualization
def get_color(value):
    return "green" if isinstance(value, (int, float)) and value >= 0 else "red"

# Create visualization
plt.figure(figsize=(10, 6))
colors = [get_color(value) for value in df_numeric["Price"]]
plt.barh(df_numeric["Category"], df_numeric["Price"], color=colors, alpha=0.8)

# Add labels
for index, value in enumerate(df_numeric["Price"]):
    plt.text
