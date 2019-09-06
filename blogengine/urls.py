from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name = 'posts_list'),
    path('post/new/', views.PostCreate.as_view(), name = 'post_create'),
    path('accounts/registration/', views.RegistrationFormView.as_view(), name = 'registration'),
    path('accounts/login/', views.LoginFormView.as_view(), name = 'login'),
    path('accounts/logout/', views.LogoutView.as_view(), name = 'logout'),
    path('accounts/profile/<str:slug>/', views.ProfileView.as_view(), name= 'profile'),
    path('accounts/profile/<str:slug>/edit/', views.ProfileUpdateView.as_view(), name= 'profile_edit'),
    path('post/<str:slug>/delete/', views.PostDelete.as_view(), name = 'post_delete'),
    path('post/<str:slug>/', views.PostDetailView.as_view(), name = 'post_detail'),
    # path('post/<str:slug>/', views.CommentCreate.as_view(), name = 'comment_create'),
    path('post/<str:slug>/edit/', views.PostEdit.as_view(), name = 'post_edit'),
]