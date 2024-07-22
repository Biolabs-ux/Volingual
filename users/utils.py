import random
from django.core.mail import EmailMessage
from .models import CustomUser, OneTimePassword
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def generateOtp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    return otp


def send_code_to_user(email):
    subject = "One time passcode for email verification"
    otp = generateOtp()
    print(otp)
    user = CustomUser.objects.get(email=email)
    current_site = "volingualAuth.me"
    email_body = f"Hello {user.first_name},\n\nYour one time passcode for email verification is {otp}. Please enter this code on the website to verify your email.\n\nIf you did not request this code, please ignore this email.\n\nRegards,\nVolingual Team"
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, otp=otp)

    d_email = EmailMessage(subject=subject, body=email_body, from_email=from_email, to=[email])
    d_email.send(fail_silently=True)


def send_normal_email(data):
    try:
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']]
        )
        email.send()
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
