import logging

import requests
from django.conf import settings
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


def send_mailgun_email(subject, recipient, template_name, context):
    if not settings.MAILGUN_API_KEY or not settings.MAILGUN_DOMAIN:
        logger.warning("Mailgun credentials missing. Skip email to %s", recipient)
        return False

    html_body = render_to_string(template_name, context)
    response = requests.post(
        f"{settings.MAILGUN_BASE_URL}/{settings.MAILGUN_DOMAIN}/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={
            "from": settings.DEFAULT_FROM_EMAIL,
            "to": [recipient],
            "subject": subject,
            "html": html_body,
        },
        timeout=settings.EMAIL_TIMEOUT,
    )
    try:
        response.raise_for_status()
    except requests.RequestException:
        logger.exception("Mailgun send failed for %s", recipient)
        return False
    return True
