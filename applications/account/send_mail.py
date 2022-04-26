from django.core.mail import send_mail


def send_mail_message(code, email):
    link = f'http://localhost:8000/account/activate/{code}'

    send_mail(
        'From django project',
        link,
        'bekbol.2019@gmail.com',
        [email]
    )

# Register, urls, Registerserializer, models activation_code


