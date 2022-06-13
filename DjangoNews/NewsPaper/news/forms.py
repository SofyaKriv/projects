from django.forms import ModelForm
from .models import Post


# Создаём модельную форму
class PostsForm(ModelForm):

    class Meta:
        model = Post
        fields = ('author', 'title_post', 'category', 'category_type', 'text_post')


