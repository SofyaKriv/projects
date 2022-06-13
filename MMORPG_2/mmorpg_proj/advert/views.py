from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .models import Post, Comments
from datetime import datetime
from .filters import CommentsFilter
from .forms import PostsForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import sub_mail, get_mail


@receiver(post_save, sender=Comments)
def sub_mail_get(sender, instance, created, **kwargs):
    if created:
        sub_mail(instance.pk)


@receiver(post_save, sender=Comments)
def get_mail_get(sender, instance, created, **kwargs):
    comment = Comments.objects.get(id=instance.pk)
    if comment.active:
        get_mail(instance.pk)


class AdvertList(ListView):
    model = Post
    template_name = 'advert.html'
    context_object_name = 'advert'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10


class SearchList(ListView):
    model = Comments
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Comments.objects.order_by('-create_date')
    form_class = SearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = CommentsFilter(self.request.GET, queryset=self.get_queryset())
        context['time_now'] = datetime.utcnow()
        context['comments'] = list(Comments.objects.filter(post__fan__user=self.request.user))
        context['form'] = SearchForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class AdvertsDetail(FormMixin, DetailView):
    model = Post
    template_name = 'advertsdetail.html'
    context_object_name = 'advertsdetail'
    queryset = Post.objects.all()
    form_class = CommentForm
    success_url = '/advert/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        context['comments'] = Comments.objects.filter(post=Post.objects.get(pk=id)).all()
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = self.get_object()
        self.object.fan = self.request.user
        self.object.save()
        post_save.connect(sub_mail_get, sender=Comments)
        return super().form_valid(form)


class PostsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'advert.add_post'
    template_name = 'post_create.html'
    form_class = PostsForm
    success_url = '/advert/'


class CommentList(ListView):
    model = Comments
    template_name = 'comments.html'
    context_object_name = 'comments'
    queryset = Comments.objects.order_by('-create_date')
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = list(Comments.objects.filter(post__fan__user=self.request.user))
        return context


class PostsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'advert.add_post'
    template_name = 'post_create.html'
    form_class = PostsForm
    success_url = '/advert/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'advert.delete_post'
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/advert/'


@login_required
def get_me(request, pk):
    comment = Comments.objects.get(id=pk)
    if not comment.active:
        comment.active = True
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unget_me(request, pk):
    comment = Comments.objects.get(id=pk)
    if comment.active:
        comment.active = False
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))




