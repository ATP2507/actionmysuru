from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_signup_email(email: str, full_name: str):
    message = MessageSchema(
        subject="Welcome to VolunteerHub!",
        recipients=[email],
        body=f"""
        <h2>Hi {full_name},</h2>
        <p>Thank you for signing up as a volunteer at <strong>VolunteerHub</strong>!</p>
        <p>Your application is currently <strong>pending approval</strong>.</p>
        <p>We will notify you once an admin reviews your application.</p>
        <br>
        <p>With gratitude,<br>The VolunteerHub Team</p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)

async def send_approval_email(email: str, full_name: str):
    message = MessageSchema(
        subject="You have been approved!",
        recipients=[email],
        body=f"""
        <h2>Congratulations {full_name}!</h2>
        <p>Your volunteer application at <strong>VolunteerHub</strong> has been <strong>approved</strong>.</p>
        <p>You can now log in to your dashboard:</p>
        <a href="http://127.0.0.1:8000/login">Click here to login</a>
        <br><br>
        <p>With gratitude,<br>The VolunteerHub Team</p>
        """,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)