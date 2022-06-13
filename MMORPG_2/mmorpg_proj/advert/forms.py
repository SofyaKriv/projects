from django.forms import ModelForm
from .models import Post, Comments, Fan
from django import forms
from django.forms.widgets import Textarea
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostsForm(ModelForm):
    text_post = forms.CharField(widget=CKEditorUploadingWidget())
    # text_post = CKEditorWidget()

    class Meta:
        model = Post
        fields = ('fan', 'title_post', 'category', 'text_post')
        # fields = '__all__'


class SearchForm(ModelForm):
    class Meta:
        model = Comments
        fields = ('fan', 'post')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget = Textarea(attrs={'rows': 5})


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        Fan.objects.create(user=user)
        basic_group = Group.objects.get(name='Fan')
        basic_group.user_set.add(user)
        return user


