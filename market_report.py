# Install required libraries
try:
    import yfinance as yf
    import pandas as pd
    import datetime
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pycoingecko import CoinGeckoAPI
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import os
    os.system("pip install yfinance pycoingecko matplotlib pandas seaborn pillow")
    import yfinance as yf
    import pandas as pd
    import datetime
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pycoingecko import CoinGeckoAPI
    from PIL import Image, ImageDraw, ImageFont

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

# Ensure numeric conversion, excluding "Date" row
df_numeric = df[df["Category"] != "Date"].copy()
df_numeric["Price"] = pd.to_numeric(df_numeric["Price"], errors="coerce")

# ========================
# 2️⃣ GENERATE HIGH-QUALITY INFOGRAPHIC
# ========================

# Set style for modern infographic
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))
colors = ["#2E86C1" if value >= 0 else "#C70039" for value in df_numeric["Price"]]
sns.barplot(x="Price", y="Category", data=df_numeric, palette=colors)

# Add labels & styling
plt.xlabel("Price", fontsize=14, fontweight="bold")
plt.ylabel("")
plt.title(f"📊 Financial Market Overview - {market_data['Date']}", fontsize=16, fontweight="bold")
plt.grid(axis="x", linestyle="--", alpha=0.5)

# Save chart as PNG
infographic_path = "financial_infographic.png"
plt.savefig(infographic_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"✅ Infographic saved as: {infographic_path}")

# ========================
# 3️⃣ ADD A HIGH-END DESIGN OVERLAY
# ========================

# Load the generated infographic
image = Image.open(infographic_path)
draw = ImageDraw.Draw(image)

# Define fonts (Replace with a path to a TTF font if needed)
try:
    font_title = ImageFont.truetype("arial.ttf", 40)
    font_labels = ImageFont.truetype("arial.ttf", 28)
except:
    font_title = None
    font_labels = None

# Add title
draw.text((50, 30), "📊 Daily Financial Market Report", fill="black", font=font_title)

# Save final image
image.save("final_financial_infographic.png")
print("🎉 Final high-quality infographic generated: final_financial_infographic.png")

# ========================
# 4️⃣ AUTOMATION SETUP (GitHub Actions or Replit)
# ========================

print("\n🚀 TO AUTOMATE THIS SCRIPT:")
print("✅ If using GitHub Actions, save this script as 'market_report.py'.")
print("✅ If using Replit, schedule this script to run at 5 AM & 5 PM.")
