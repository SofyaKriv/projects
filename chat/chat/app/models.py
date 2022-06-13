from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = RichTextUploadingField(default='')

    def __str__(self):
        return self.user.username


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)


class Room(models.Model):
    room_name = models.TextField(verbose_name='Название комнаты')
    participants = models.ManyToManyField(User, blank=True, null=True)
    # messages = models.TextField(verbose_name='Сообщение')

    def get_absolute_url(self):
        return f'/{self.id}'


class Room_message(models.Model):
    send = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room')
    text = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)





