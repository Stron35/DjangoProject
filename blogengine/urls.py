from django.urls import path
from . import views

urlpatterns = [
	path('', views.post_list, name = 'posts_list'),
	path('post/new/', views.PostCreate.as_view(), name = 'post_create'),
	path('post/<str:slug>/', views.post_detail, name = 'post_detail'),
	path('post/<str:slug>/edit/', views.PostEdit.as_view(), name = 'post_edit'),
]