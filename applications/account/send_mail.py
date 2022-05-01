from django.core.mail import send_mail


def mail_message(code, email,):
    # if status == 'register':
    link = f'http://localhost:8000/api/v1/element/activate/{code}'

    send_mail(
        'From django project',
        link,
        'bekbol.2019@gmail.com',
        [email]
    )
# Register, urls, Registerserializer, models activation_code


