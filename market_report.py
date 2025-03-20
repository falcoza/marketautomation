import os
import smtplib
from email.message import EmailMessage

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "ypanchia@gmail.com"  # Replace with your actual Gmail
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Securely use GitHub Secret
EMAIL_RECEIVER = "yeshiel@dailymaverick.co.za"

def send_email():
    if not EMAIL_PASSWORD or EMAIL_PASSWORD.strip() == "":
        raise ValueError("❌ ERROR: EMAIL_PASSWORD environment variable is missing! Check GitHub Secrets.")

    msg = EmailMessage()
    msg["Subject"] = "📊 Daily Financial Market Infographic"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content("Attached is your latest financial market infographic. 📈📊")

    infographic_path = "final_financial_infographic.png"
    with open(infographic_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="image", subtype="png", filename="financial_infographic.png")

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

send_email()
