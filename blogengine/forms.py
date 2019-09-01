from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('bio', 'userImage')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'text': forms.Textarea(attrs={'class':'materialize-textarea','placeholder':'Write post text here'}),
        }


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length= 50,label='Username',label_suffix = '', widget = forms.TextInput(attrs={'class':'form-control',
        'placeholder':'Enter your username'}))
    email = forms.EmailField(max_length = 150, label='E-mail',label_suffix = '',
        widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Enter a valid email address'}))
    password1=forms.CharField(label='Password',label_suffix = '', widget = forms.PasswordInput(attrs={'class': 'form-control',
        'placeholder': 'Password'}))
    password2=forms.CharField(label='Password again', label_suffix = '', widget = forms.PasswordInput(attrs={'class': 'form-control',
        'placeholder': 'Password again'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username',label_suffix = '', widget= forms.TextInput(attrs={'class':'form-control',
        'placeholder':'Enter your username', 'label':'Username'}))
    password = forms.CharField(label='Password',label_suffix = '', widget = forms.PasswordInput(attrs={'class': 'form-control',
        'placeholder': 'Password',}))

    class Meta:
        model = User
        fields = ('username', 'password')