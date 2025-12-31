import json
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

load_dotenv()


# NOTE: For security reasons, sensitive information like credentials
# MUST be loaded from secure environment variables or a configuration service
# and NEVER stored directly in code.

# --- CONFIGURATION FOR GMAIL SMTP ---
# Use an "App Password" from your Google Account settings, NOT your main password.
# SMTP_SERVER = "smtp.gmail.com" 
# SMTP_PORT = 465  # Use 465 for SSL/TLS
# SENDER_EMAIL = "your.standard.gmail@gmail.com" # <-- Replace with your actual sending Gmail address
# SENDER_PASSWORD = "YOUR_GMAIL_APP_PASSWORD"  # <-- Replace with your generated App Password
# TARGET_EMAIL = "aj2524113@gmail.com" # The recipient email address

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
TARGET_EMAIL = os.getenv("TARGET_EMAIL")

# --- CORE FUNCTION ---

def send_mail(
    target_email: str, 
    subject: str, 
    source: str, 
    form_data: Dict[str, Any]
) -> bool:
    """
    Sends an email using Python's smtplib via a configured SMTP server (like Gmail).

    :param target_email: The destination email address (e.g., support@yourcompany.com).
    :param subject: The subject line of the email.
    :param source: The source of the form submission ('Join Us' or 'Contact').
    :param form_data: A dictionary containing all fields submitted by the user.
    :return: True if the email was sent successfully, False otherwise.
    """
    
    print(f"--- Processing Submission from: {source} ---")
    print(f"Target Email: {target_email}")
    print(f"Subject: {subject}")
    print(f"Data Received: {json.dumps(form_data, indent=2)}")

    # 1. Construct Email Body (The content the support team will read)
    body_lines = [f"A new submission was received from the {source} form.", "\n--- Details ---"]
    for key, value in form_data.items():
        # Capitalize the key for better readability in the email
        readable_key = key.replace('_', ' ').capitalize()
        body_lines.append(f"{readable_key}: {value}")
    
    email_body_plain = "\n".join(body_lines)
    email_body_html = email_body_plain.replace('\n', '<br>')
    
    # 2. Build the Email Message Object
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = target_email

    # Attach both plain text and HTML versions
    message.attach(MIMEText(email_body_plain, "plain"))
    message.attach(MIMEText(email_body_html, "html"))
    
    # 3. Send the email via SMTP
    context = ssl.create_default_context()
    
    try:
        # Use SMTP_SSL for connection on port 465
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            # Login to the server
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            # Send the mail
            server.sendmail(SENDER_EMAIL, target_email, message.as_string())
        
        print("SUCCESS: Email sent successfully via SMTP.")
        return True
    
    except smtplib.SMTPAuthenticationError:
        print("CRITICAL FAILURE: SMTP Authentication failed. Check SENDER_EMAIL/SENDER_PASSWORD (App Password).")
        return False
    except smtplib.SMTPServerDisconnected:
        print(f"CRITICAL FAILURE: SMTP Server Disconnected. Check server address/port ({SMTP_SERVER}:{SMTP_PORT}).")
        return False
    except Exception as e:
        print(f"CRITICAL FAILURE: An unexpected error occurred during email sending: {e}")
        return False

# --- EXAMPLE USAGE (For testing the function separately) ---

class MailRequest(BaseModel):
    target_email: str = TARGET_EMAIL
    subject: str
    source: str
    form_data: Dict[str, Any]

app = FastAPI()
# allow local frontend to call the API while developing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/send-mail")
def api_send_mail(req: MailRequest):
    """
    Accepts JSON and forwards to send_mail(). Returns success: true/false.
    """
    success = send_mail(
        target_email= TARGET_EMAIL,
        subject=req.subject,
        source=req.source,
        form_data=req.form_data
    )
    return {"success": success}

if __name__ == "__main__":
    # Start server for local development
    uvicorn.run(app, host="0.0.0.0", port=8000)