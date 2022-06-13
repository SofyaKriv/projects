from django.core.mail import send_mail
import datetime
from .models import User, Post
from django.template.loader import render_to_string
from celery import shared_task
import logging


@shared_task
def send_mails():
    end_date = datetime.datetime.now().date()
    start_date = end_date - datetime.timedelta(days=7)
    print('Выполнение началось')
    for user in User.objects.all():
        email = user.email
        if len(user.category_set.all()) > 0:
            list_of_posts = Post.objects.filter(time_creation__range=(start_date, end_date),
                                                category__in=user.category_set.all())
            html_content = render_to_string(
                'sub_week.html',
                {
                    'news': list_of_posts,
                    'user': user,
                }
            )
            send_mail(
                    subject="Новые статьи за неделю",
                    message=f'{user}, в Вашей любимой категории новые статьи.',
                    from_email='test250621@yandex.ru',
                    recipient_list=[email],
                    html_message=html_content
            )
    # print("Hello from scheduler")


@shared_task
def sub_mail(objid):
    post = Post.objects.get(id=objid)
    for user in User.objects.all():
        if post.category in user.category_set.all():
            try:
                subject = post.title_post
                send_mail(
                    subject=subject,
                    message=f'В Вашей любимой категории новая статья {subject}: ' + post.text_post + f" http://127.0.0.1:8000/news/{post.id}",
                    from_email='test250621@yandex.ru',
                    recipient_list=[user.email]
                )
            except post.DoesNotExist:
                logging.warning("Tried to send non-existing email '%s'" % objid)

