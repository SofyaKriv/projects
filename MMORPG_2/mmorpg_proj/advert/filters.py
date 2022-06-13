from django_filters import FilterSet
from .models import Comments
import django_filters
from django import forms


class CommentsFilter(FilterSet):
    fan = django_filters.CharFilter(
        field_name='fan__username',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Автор'}),
    )
    post = django_filters.CharFilter(
        field_name='post__title_post',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
    )

    class Meta:
        model = Comments
        fields = ['post', 'fan']
