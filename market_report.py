import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from PIL import Image, ImageDraw, ImageFont

# ✅ Email Configuration (Gmail SMTP)
EMAIL_SENDER = "ypanchia@gmail.com"  # 🔹 Replace with your Gmail
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # 🔹 Securely use GitHub Secret
EMAIL_RECEIVER = "yeshiel@dailymaverick.co.za"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ✅ Design Constants (Daily Maverick Theme)
BACKGROUND_COLOR = "#FFFFFF"
TEXT_COLOR = "#1D1D1B"
HEADER_COLOR = "#B31B1B"
TABLE_BORDER_COLOR = "#D3D3D3"

# ✅ Fetch Market Data
def get_market_data():
    """Retrieve live market data from Yahoo Finance & CoinGecko."""
    try:
        # Fetch JSE ALSI data
        jse = yf.Ticker("^JN0U.JO")  # JSE All Share Index
        jse_price = jse.history(period="1d")["Close"].iloc[-1] if not jse.history(period="1d").empty else None

        # Fetch Forex rates
        forex_rates = {
            "Rand / Dollar": yf.Ticker("USDZAR=X").history(period="1d")["Close"].iloc[-1],
            "Rand / Euro": yf.Ticker("EURZAR=X").history(period="1d")["Close"].iloc[-1],
            "Rand / GBP": yf.Ticker("GBPZAR=X").history(period="1d")["Close"].iloc[-1],
        }

        # Fetch Commodity Prices
        commodities = {
            "Brent ($/barrel)": yf.Ticker("BZ=F").history(period="1d")["Close"].iloc[-1],
            "Gold ($/oz)": yf.Ticker("GC=F").history(period="1d")["Close"].iloc[-1],
        }

        # Fetch S&P 500
        sp500 = yf.Ticker("^GSPC").history(period="1d")["Close"].iloc[-1]

        # Fetch Bitcoin Price (CoinGecko)
        cg = CoinGeckoAPI()
        bitcoin_price = cg.get_price(ids="bitcoin", vs_currencies="zar")["bitcoin"]["zar"]

        # ✅ Store Data
        data = {
            "JSE All Share": jse_price,
            "Rand / Dollar": forex_rates["Rand / Dollar"],
            "Rand / Euro": forex_rates["Rand / Euro"],
            "Rand / GBP": forex_rates["Rand / GBP"],
            "Brent ($/barrel)": commodities["Brent ($/barrel)"],
            "Gold ($/oz)": commodities["Gold ($/oz)"],
            "S&P 500": sp500,
            "Rand / Bitcoin": bitcoin_price,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        return data

    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        return None


# ✅ Generate Infographic
def create_infographic(data):
    """Generates a financial infographic using a table layout."""
    df = pd.DataFrame(data.items(), columns=["Category", "Price"])
    df_numeric = df[df["Category"] != "Date"].copy()
    df_numeric["Price"] = pd.to_numeric(df_numeric["Price"])

    # ✅ Set Up Image Canvas
    img_width, img_height = 900, 600
    img = Image.new("RGB", (img_width, img_height), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    # ✅ Load Georgia Font
    try:
        font_title = ImageFont.truetype("Georgia.ttf", 36)
        font_table_header = ImageFont.truetype("Georgia.ttf", 24)
        font_table_text = ImageFont.truetype("Georgia.ttf", 22)
    except IOError:
        print("⚠️ Georgia font not found. Using default font.")
        font_title = ImageFont.load_default()
        font_table_header = ImageFont.load_default()
        font_table_text = ImageFont.load_default()

    # ✅ Title
    title_text = f"📊 Market Report - {data['Date']}"
    draw.text((img_width // 2 - 200, 20), title_text, font=font_title, fill=TEXT_COLOR)

    # ✅ Draw Table Headers
    header_y = 80
    draw.rectangle([(50, header_y), (850, header_y + 40)], fill=HEADER_COLOR)
    draw.text((100, header_y + 5), "Category", font=font_table_header, fill="white")
    draw.text((600, header_y + 5), "Value", font=font_table_header, fill="white")

    # ✅ Draw Table Data
    row_height = 50
    y_position = header_y + 50

    for index, row in df_numeric.iterrows():
        row_color = "#F5F5F5" if index % 2 == 0 else "#FFFFFF"
        draw.rectangle([(50, y_position), (850, y_position + row_height)], fill=row_color)
        draw.text((100, y_position + 10), row["Category"], font=font_table_text, fill=TEXT_COLOR)
        draw.text((600, y_position + 10), f"{row['Price']:.2f}", font=font_table_text, fill=TEXT_COLOR)
        y_position += row_height

    # ✅ Save Infographic
    infographic_path = "financial_infographic.png"
    img.save(infographic_path)
    print(f"✅ Infographic saved as: {infographic_path}")


# ✅ Send Infographic via Email
def send_email():
    """Emails the financial infographic using Gmail SMTP."""
    if not EMAIL_PASSWORD:
        raise ValueError("❌ ERROR: EMAIL_PASSWORD environment variable is missing! Check GitHub Secrets.")

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "📊 Daily Financial Report"

    body = "Attached is the latest financial infographic report."
    msg.attach(MIMEText(body, "plain"))

    infographic_path = "financial_infographic.png"
    if not os.path.exists(infographic_path):
        raise FileNotFoundError("❌ ERROR: financial_infographic.png not found!")

    with open(infographic_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename=financial_infographic.png")
        msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("✅ Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        raise ValueError("❌ ERROR: SMTP Authentication failed! Check your Gmail App Password.")


# ✅ Run Full Script
if __name__ == "__main__":
    print("🚀 Fetching market data...")
    market_data = get_market_data()

    if market_data:
        print("📊 Generating infographic...")
        create_infographic(market_data)

        # ✅ Email the report
        print("📩 Sending infographic via email...")
        send_email()

        print("🎉 Process complete! Check 'financial_infographic.png'.")
    else:
        print("❌ Market data retrieval failed. Skipping infographic and email.")
