import logging

logger = logging.getLogger("email")


def send_email(to: str, subject: str, body: str) -> None:
    logger.info("E-mail para %s | Assunto: %s | Corpo: %s", to, subject, body)
