from django.urls import path
from . import views

urlpatterns = [
	path('', views.post_list, name = 'posts_list'),
	path('post/new/', views.PostCreate.as_view(), name = 'post_create'),
	path('accounts/registration/', views.RegistrationFormView.as_view(), name = 'registration'),
	path('accounts/login/', views.LoginFormView.as_view(), name = 'login'),
	path('accounts/logout/', views.LogoutView.as_view(), name = 'logout'),
	# path('accounts/profile/', views.update_profile, name= 'profile'),
	path('post/<str:slug>/delete/', views.PostDelete.as_view(), name = 'post_delete'),
	path('post/<str:slug>/', views.post_detail, name = 'post_detail'),
	path('post/<str:slug>/edit/', views.PostEdit.as_view(), name = 'post_edit'),
]