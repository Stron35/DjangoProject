from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'text',)


class RegisterForm(UserCreationForm):
	email = forms.EmailField(max_length = 150, help_text = 'Required')
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

#class LoginForm(AuthenticationForm):