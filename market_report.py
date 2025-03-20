# Install required libraries
try:
    import yfinance as yf
    import pandas as pd
    import datetime
    import matplotlib.pyplot as plt
    import seaborn as sns
    from pycoingecko import CoinGeckoAPI
    from PIL import Image, ImageDraw, ImageFont
    import smtplib
    import os
    from email.message import EmailMessage
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
    import smtplib
    from email.message import EmailMessage

# ========================
# 1️⃣ DEBUG ENVIRONMENT VARIABLES
# ========================

print("🔍 DEBUG: Checking environment variables...")

for key, value in os.environ.items():
    print(f"{key}: {'SET' if value else 'NOT SET'}")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if not EMAIL_PASSWORD:
    raise ValueError("❌ ERROR: EMAIL_PASSWORD environment variable is missing! Check GitHub Secrets.")

print("✅ EMAIL_PASSWORD is detected in the environment.")

# ========================
# 2️⃣ FETCH MARKET DATA
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
# 3️⃣ GENERATE HIGH-QUALITY INFOGRAPHIC
# ========================

# Set style for modern infographic
sns.set_style("whitegrid")
plt.figure(figsize=(12, 6))

# Fix Seaborn warning
sns.barplot(x="Price", y="Category", data=df_numeric, hue="Category", legend=False, palette="coolwarm")

# Add labels & styling
plt.xlabel("Price", fontsize=14, fontweight="bold")
plt.ylabel("")
plt.title(f"📊 Financial Market Overview - {market_data['Date']}", fontsize=16, fontweight="bold")
plt.grid(axis="x", linestyle="--", alpha=0.5)

# Fix font issue
plt.rcParams["font.family"] = "Arial"

# Save chart as PNG
infographic_path = "financial_infographic.png"
plt.savefig(infographic_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"✅ Infographic saved as: {infographic_path}")

# ========================
# 4️⃣ ADD A HIGH-END DESIGN OVERLAY
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
final_image_path = "final_financial_infographic.png"
image.save(final_image_path)
print("🎉 Final high-quality infographic generated: final_financial_infographic.png")

# ========================
# 5️⃣ EMAIL INFOGRAPHIC
# ========================

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "ypanchia@gmail.com"  # Replace with your Gmail
EMAIL_RECEIVER = "yeshiel@dailymaverick.co.za"

def send_email():
    if not EMAIL_PASSWORD:
        raise ValueError("❌ ERROR: EMAIL_PASSWORD environment variable is missing! Check GitHub Secrets.")

    msg = EmailMessage()
    msg["Subject"] = "📊 Daily Financial Market Infographic"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content("Attached is your latest financial market infographic. 📈📊")

    # Attach the infographic
    with open(final_image_path, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="image", subtype="png", filename="financial_infographic.png")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("📧 Email sent successfully!")
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP Authentication Error: {e}")
        print("🔴 Check if your Gmail App Password is correct.")
        print("🔴 If using 2FA, generate a new App Password.")
        print("🔴 Make sure `EMAIL_PASSWORD` is added correctly in GitHub Secrets.")

# Call the function after generating the infographic
send_email()
