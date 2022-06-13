from django.urls import path
import allauth.account.views
from .views import NewsList, NewsDetail, SearchList, CategoryList, PostsCreateView, PostsUpdateView, PostsDeleteView, upgrade_me, subscribe_me, unsubscribe_me


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='newsdetail'),
    path('search/', SearchList.as_view(), name='search'),
    path('create/', PostsCreateView.as_view(), name='post_create'),
    path('create/<int:pk>', PostsUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostsDeleteView.as_view(), name='post_delete'),
    path('accounts/upgrade/', upgrade_me, name='upgrade'),
    path('accounts/login/', allauth.account.views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('category/', CategoryList.as_view()),
    path('subscribe/<int:pk>', subscribe_me),
    path('unsubscribe/<int:pk>', unsubscribe_me),
    path('category/subscribe/<int:pk>', subscribe_me),
    path('category/unsubscribe/<int:pk>', unsubscribe_me),
]