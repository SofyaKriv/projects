from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Fan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Category(models.Model):
    theme = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.theme}'


class Post(models.Model):
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, verbose_name='Автор')
    time_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    title_post = models.CharField(max_length=255, verbose_name='Заголовок')
    # text_post = models.CharField(max_length=255, default="Объявление пустое", verbose_name='Содержание')
    text_post = RichTextUploadingField()

    def preview(self):
        return self.text_post[0:124] + '...'

    def __str__(self):
        return f'{self.title_post.title()}: {self.text_post}'

    def get_absolute_url(self):
        return f'/advert/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление', blank=True, null=True, related_name='comments')
    fan = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField(verbose_name='Текст комментария')
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{}: {}'.format(self.fan, self.text)



