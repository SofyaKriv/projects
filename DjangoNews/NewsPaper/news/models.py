from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.user}'

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum("rate_post"))
        pRat = 0
        pRat += int(postRat.get("postRating") or 0)
        commentRat = self.user.comment_set.aggregate(commentRating=Sum("rate_comment"))
        cRat = 0
        cRat += int(commentRat.get("commentRating") or 0)
        self.user_rating = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    theme = models.CharField(max_length=255, unique=True)
    subscriber = models.ManyToManyField(User, blank=True, null=True)


class Post(models.Model):
    news = "Новость"
    article = "Статья"
    CategoryType = (
        (news, "Новость"),
        (article, "Статья"),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_type = models.CharField(max_length=7, choices=CategoryType, default=news)
    time_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title_post = models.CharField(max_length=255)
    text_post = models.TextField(default="Статья пустая")
    rate_post = models.IntegerField(default=0, null=True)

    def like(self):
        self.rate_post = self.rate_post + 1
        self.save()

    def dislike(self):
        self.rate_post -= Post.objects.get(id=1).rate_post
        self.save()

    def preview(self):
        return self.text_post[0:124] + '...'

    def __str__(self):
        return f'{self.title_post.title()}: {self.text_post}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    date_comment = models.DateTimeField(auto_now_add=True)
    rate_comment = models.IntegerField(default=0, null=True)

    def like(self):
        self.rate_comment = self.rate_comment + 1
        self.save()

    def dislike(self):
        self.rate_comment -= Comment.objects.get(id=1).rate_comment
        self.save()
