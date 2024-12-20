from pathlib import Path
from typing import Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from .. import settings

BASE_DIR = Path(__file__).resolve().parent.parent

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_FROM=settings.mail_sender_email,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    MAIL_STARTTLS=False,
    TEMPLATE_FOLDER=BASE_DIR / "templates",
)


async def send_email(
    subject: str, email_to: str, template_name: str, body: Optional[dict]
):
    """Function to send emails asynchronously"""
    try:
        print(settings.mail_sender_email)
        message = MessageSchema(
            subject=subject,
            recipients=[email_to],
            template_body=body,
            subtype=MessageType.html,
        )
        fm = FastMail(mail_config)
        await fm.send_message(message, template_name=template_name)

    except Exception as e:
        print(e)
        raise Exception
