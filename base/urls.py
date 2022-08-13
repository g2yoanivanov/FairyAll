from django.urls import path
from base import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),

    path('', views.home, name='home'),
    path('authors/<str:pk>/', views.author_profile, name='author-profile'),
    path('tales/<str:pk>/', views.tale, name='tale'),
]

