from django.urls import path
from base import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_page, name='register'),

    path('users/<str:pk>/', views.user_profile, name='user-profile'),
    path('update-user/', views.update_user, name="update-user"),

    path('', views.home, name='home'),
    path('authors/<str:pk>/', views.author_profile, name='author-profile'),
    path('tales/<str:pk>/', views.tale, name='tale'),

    path('forum/', views.forum, name='forum',),
    path('delete-message/<str:pk>/', views.delete_message, name='delete-message'),

    path('create-tale/', views.create_tale, name='create-tale'),
    path('update-tale/<str:pk>/', views.update_tale, name='update-tale'),
    path('delete-tale/<str:pk>/', views.delete_tale, name='delete-tale'),
    path('tales/', views.all_tales, name='all-tales'),

    path('create-author/', views.create_author, name='create-author'),
    path('update-author/<str:pk>/', views.update_author, name='update-author'),
    path('delete-author/<str:pk>/', views.delete_author, name='delete-author'),
    path('authors/', views.all_authors, name='all-authors'),
]

