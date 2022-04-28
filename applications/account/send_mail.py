from django.core.mail import send_mail


def send_mail_message(code, email, status):
    if status == 'register':
        link = f'http://localhost:8000/account/activate/{code}'

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

# Register, urls, Registerserializer, models activation_code


