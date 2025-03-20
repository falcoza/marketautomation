import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ✅ Securely fetch the email password
EMAIL_SENDER = "ypanchia@gmail.com"  # Replace with your Gmail
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # Securely use GitHub Secret

if not EMAIL_PASSWORD:
    raise ValueError("❌ ERROR: EMAIL_PASSWORD environment variable is missing! Check GitHub Secrets.")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_RECEIVER = "yeshiel@dailymaverick.co.za"

def send_email():
    """Send an email with the financial infographic."""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "📊 Daily Financial Report"

    body = "Attached is the latest financial infographic report."
    msg.attach(MIMEText(body, "plain"))

    # Attach infographic (if generated)
    with open("financial_infographic.png", "rb") as attachment:
        from email.mime.base import MIMEBase
        from email import encoders
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

# Execute email sending
send_email()
