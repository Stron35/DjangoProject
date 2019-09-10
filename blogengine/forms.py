from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Post, User, Comment

# class UserEditForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ('userImage','bio')
#         slug_field = 'username'
        


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'text': forms.Textarea(attrs={'placeholder':'Write post text here'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'placeholder':'Write comment text here'})
        }


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length= 50,label='Username',label_suffix = '',
        widget = forms.TextInput(attrs={'placeholder':'Enter your username'}))
    email = forms.EmailField(max_length = 150, label='E-mail',label_suffix = '',
        widget = forms.EmailInput(attrs={'placeholder':'Enter a valid email address'}))
    password1=forms.CharField(label='Password',label_suffix = '',
        widget = forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2=forms.CharField(label='Password again', label_suffix = '',
        widget = forms.PasswordInput(attrs={'placeholder': 'Password again'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username',label_suffix = '', widget= forms.TextInput(attrs={'placeholder':'Enter your username', 'label':'Username'}))
    password = forms.CharField(label='Password',label_suffix = '', widget = forms.PasswordInput(attrs={'placeholder': 'Password',}))

    class Meta:
        model = User
        fields = ('username', 'password')