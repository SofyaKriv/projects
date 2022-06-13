from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from datetime import datetime
from .filters import PostFilter
from .forms import PostsForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import sub_mail

import logging

logger = logging.getLogger(__name__)


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        try:
            premium_group.user_set.add(user)
        except Exception as e:
            logger.error('Ошибка операции')
    return redirect('/news/')


@receiver(post_save, sender=Post)
def sub_mail_get(sender, instance, created, **kwargs):
    if created:
        sub_mail.apply_async([instance.pk], countdown=10)


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        logger.info('Работаем')
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['value1'] = None
        return context


class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-time_creation')
    form_class = PostsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['time_now'] = datetime.utcnow()  # добавим переменную текущей даты time_now
        context['categories'] = Category.objects.all()
        context['form'] = PostsForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class NewsDetail(DetailView):
    model = Post
    template_name = 'newsdetail.html'
    context_object_name = 'newsdetail'
    queryset = Post.objects.all()


class PostsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    template_name = 'post_create.html'
    form_class = PostsForm
    success_url = '/news/'

    # def form_valid(self, form):
    #     post = form.save()
    #     sub_mail.apply_async([post.pk], countdown=10)
    #     # sub_mail.delay(10)
    #     return redirect('/news')
    #     # sub_mail.apply_async([post.pk], countdown=10)
    post_save.connect(sub_mail_get, sender=Post)


class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categorys'
    paginate_by = 5


@login_required
def subscribe_me(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category not in user.category_set.all():
        category.subscriber.add(user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_me(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category in user.category_set.all():
        category.subscriber.remove(user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


class PostsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.add_post'
    template_name = 'post_create.html'
    form_class = PostsForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

