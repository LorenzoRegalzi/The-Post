from django.urls import path
from . import views


urlpatterns = [
    path('', views.signin, name='signin'),
    path('home', views.home, name='home'),
    path('logout', views.logout_user, name='logout'),
    path('signup', views.signup, name='signup'),
    path('post/new/', views.post_new, name='post_new'),
    path('table/posts', views.table_posts, name='table_posts'),
    path('api/post', views.last_hour_post, name='last_hour_post'),
    path('user/<int:id>', views.user_page, name='user_page'),
    path('find/word/<str:word>', views.find_word, name='find_word')
]

