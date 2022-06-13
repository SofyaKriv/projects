from django.forms import ModelForm
from .models import UserProfile, Room
from django import forms
from django.forms.widgets import Textarea
from django.contrib.auth.models import Group
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ProfileForm(ModelForm):
    avatar = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = UserProfile
        fields = ('user', 'avatar',)


class RoomForm(ModelForm):

    class Meta:
        model = Room
        fields = ('room_name', 'participants',)
