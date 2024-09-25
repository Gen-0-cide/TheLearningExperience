from django.core.mail import send_mail
import random


def send_confirmation_code(email):
    code = random.randint(100000, 999999)

    Cache.set(f'confirmation_code_{email}', code, timeout=60)

    subject = 'Ваш код подтверждения'
    message = f'Ваш одноразовый код подтверждения: {code}'
    from_email = '96bat69@rambler.ru'


    send_mail(subject, message, from_email, [email])

    return code
