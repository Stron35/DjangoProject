from django.urls import path, include
from . import views

# path('accounts/', include('django.contrib.auth.urls')):
# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']

urlpatterns = [
    path('', views.post_list, name = 'posts_list'),
    path('post/new/', views.PostCreate.as_view(), name = 'post_create'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/registration/', views.RegistrationFormView.as_view(), name = 'registration'),
    path('accounts/activate/<uidb64>/<token>/', views.activate_account, name = 'activate_account'),
    path('accounts/profile/<str:slug>/', views.ProfileView.as_view(), name= 'profile'),
    path('accounts/profile/<str:slug>/edit/', views.ProfileUpdateView.as_view(), name= 'profile_edit'),
    path('post/<str:slug>/delete/', views.PostDelete.as_view(), name = 'post_delete'),
    path('post/<str:slug>/', views.PostDetailView.as_view(), name = 'post_detail'),
    path('post/<str:slug>/edit/', views.PostEdit.as_view(), name = 'post_edit'),
    path('post/<str:slug>/comment/<int:id>/delete/', views.CommentDelete.as_view(), name = 'comment_delete'),
]