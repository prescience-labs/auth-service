from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import get_template

def send_password_reset_email(user, from_email=settings.DEFAULT_FROM_EMAIL):
    """Send a password reset email to the given user."""
    template = get_template('common/emails/password_reset.html')
    html_email = template.render({'button_link':user.password_reset_token})

    email = EmailMultiAlternatives(
        to=[user.email],
        subject='ACTION REQUIRED: Password reset',
        body=f"Someone initiated a password reset for you. If it wasn't you, don't worry about it. If it was, use this link to reset your password: {user.password_reset_token}",
        from_email=from_email,
    )
    email.attach_alternative(html_email, 'text/html')
    email.content_subtype = 'html'
    return email.send()
