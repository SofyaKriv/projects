from django.core.mail import send_mail
from .models import Comments
from celery import shared_task
import logging


@shared_task
def sub_mail(objid):
    print("Письмо отправлено")
    comment = Comments.objects.get(id=objid)
    try:
        subject = comment.post
        send_mail(
            subject=subject,
            message=f'На Ваше объявление откликнулись: ' + comment.text + f" http://127.0.0.1:8000/advert/{subject.id}",
            from_email='test250621@yandex.ru',
            recipient_list=[comment.post.fan.user.email]
        )
    except comment.DoesNotExist:
        logging.warning("Tried to send non-existing email '%s'" % objid)


@shared_task
def get_mail(objid):
    comment = Comments.objects.get(id=objid)
    try:
        subject = comment.post
        send_mail(
            subject=subject,
            message='Ваш комментарий: ' + comment.text + ' - принят',
            from_email='test250621@yandex.ru',
            recipient_list=[comment.fan.email]
        )
    except comment.DoesNotExist:
        logging.warning("Tried to send non-existing email '%s'" % objid)