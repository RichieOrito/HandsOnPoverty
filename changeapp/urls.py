from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
    path('',views.welcome, name="index"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('profile/<str:username>/', views.profile, name = 'profile'),
    path('update_profile', views.update_profile, name="update_profile"),
    path('post/article', views.article, name='newArticle'),
    path('delete/article/<int:id>', views.delete_article, name = 'delete_article'),
    path('edit/article/<int:id>', views.update_article, name ='update_article'),
    path('article/<int:id>', views.single_article, name = 'single_article'),
    path('articles/health', views.health_articles, name = 'heath_articles'),
    path('articles/water', views.water_articles, name = 'water_articles'),
    path('articles/water', views.education_articles, name = 'education_articles'),
    path('article/comment/<int:id>', views.add_comment, name='add_comment'),
    path('online/lipa', views.lipa_na_mpesa_online, name='lipa_na_mpesa'),
    # register, confirmation, validation and callback urls
    path('c2b/register', views.register_urls, name="register_mpesa_validation"),
    path('c2b/confirmation', views.confirmation, name="confirmation"),
    path('c2b/validation', views.validation, name="validation"),
    path('c2b/callback', views.call_back, name="call_back"),

]
