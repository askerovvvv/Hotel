import time

from celery import shared_task
from django.core.mail import send_mail

# @shared_task
from .celery import app


@app.task
def send_mail_message(code, email, status):
    time.sleep(5)
    link = f'http://localhost:8000/account/activate/{code}'

    if status == 'register':

        send_mail(
            'From django project',
            link,
            'bekbol.2019@gmail.com',
            [email]
        )
    elif status == 'reset_password':
        send_mail(
            'Reset your password',
            f'Code activations: {code}',
            'stackoverflow@gmail.com',
            [email]
        )
    elif status == 'reserv':
        send_mail(
            'From django project',
            link,
            'bekbol.2019@gmail.com',
            [email]
        )



