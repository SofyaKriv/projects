from django_filters import FilterSet
from .models import Post
import django_filters
from django import forms


class PostFilter(FilterSet):
    author = django_filters.CharFilter(
        field_name='author',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Автор'}),
    )

    time_creation = django_filters.DateFilter(
        field_name='time_creation',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        lookup_expr='gt',
    )
    title_post = django_filters.CharFilter(
        field_name='title_post',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
    )

    class Meta:
        model = Post
        fields = ['time_creation', 'title_post', 'author']