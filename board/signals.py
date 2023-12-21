import logging

from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from board.models import Response


@receiver(post_save, sender=Response)
def response_save(instance, created, **kwargs):
    logging.debug('Создан отклик')
    if not created:
        text_response = instance.text
        email = instance.created_by.email
        ad = instance.ad
        ad_title = ad.title

        subject = f'Ваш отклик принят'
        text_content = (
            f'На объявление {ad_title} принят Ваш отклик.'
            f'Текст отклика: {text_response}'
            f'Ссылка на объявление: http://127.0.0.1:8000{ad.get_absolute_url()}'
        )
        html_content = (
            f'На объявление {ad_title} принят Ваш отклик.'
            f'Текст отклика: {text_response}'
            f'<a href="http://127.0.0.1{ad.get_absolute_url()}">'
            f'Ссылка на объявление</a>'
        )
    elif created:
        user = instance.ad.created_by
        email = user.email
        ad_title = instance.ad.title

        subject = f'На ваше объявление {ad_title} оставлен отклик'

        text_content = (
            f'На ваше объявление {ad_title} оставлен отклик.'
            'Вы можете посмотреть его в своем личном кабинете.'
            f'Ссылка на личный кабинет: http://127.0.0.1:8000/accounts/user/{user.username}'
        )
        html_content = (
            f'На ваше объявление {ad_title} оставлен отклик.'
            'Вы можете посмотреть его в своем личном кабинете.'
            f'<a href="http://127.0.0.1:8000/accounts/user/{user.username}">'
            f'Ссылка на личный кабинет</a>'
        )
    else:
        return

    msg = EmailMultiAlternatives(subject, text_content, None, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
