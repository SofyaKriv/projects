from django.urls import path
import allauth.account.views
from .views import AdvertList, AdvertsDetail, SearchList, PostsCreateView, PostsUpdateView, PostsDeleteView, CommentList, get_me, unget_me


urlpatterns = [
    path('', AdvertList.as_view()),
    path('<int:pk>', AdvertsDetail.as_view(), name='advertsdetail'),
    path('comments/search/', SearchList.as_view(), name='search'),
    path('create/', PostsCreateView.as_view(), name='post_create'),
    path('create/<int:pk>', PostsUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostsDeleteView.as_view(), name='post_delete'),
    path('accounts/login/', allauth.account.views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', allauth.account.views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('comments/', CommentList.as_view(), name="comments"),
    path('get/<int:pk>', get_me),
    path('unget/<int:pk>', unget_me),
    path('comments/get/<int:pk>', get_me),
    path('comments/unget/<int:pk>', unget_me),

]