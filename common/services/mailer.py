import requests
from django.conf import settings

class Email:
    api_key = settings.MAILGUN_API_KEY
    domain_name = settings.MAILGUN_DOMAIN_NAME
    from_email = settings.FROM_EMAIL
    to_email = ''
    subject = ''
    content = ''

    def __init__(self, to_email, subject, content, from_email=settings.FROM_EMAIL):
        self.to_email = to_email
        self.subject = subject
        self.content = content
        self.from_email = from_email

    def send(self):
        return requests.post(
            f'https://api.mailgun.net/v3/{self.domain_name}/messages',
            auth=('api', self.api_key),
            data={
                'from': self.from_email,
                'to': [self.to_email],
                'subject': self.subject,
                'text': self.content,
            }
        )
