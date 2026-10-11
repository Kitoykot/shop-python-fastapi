import smtplib
from email.message import EmailMessage


class MailService:
    def __init__(self, host: str, port: int, sender: str):
        self.host = host
        self.port = port
        self.sender = sender

    def send(self, recipient: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message['From'] = self.sender
        message['To'] = recipient
        message['Subject'] = subject
        message.set_content(body)

        with smtplib.SMTP(
            host=self.host,
            port=self.port,
            timeout=5,
        ) as client:
            client.send_message(message)
