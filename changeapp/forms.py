from dataclasses import field, fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Articles, User
from django import forms


        

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']   

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        exclude = ['author', 'date_posted']

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ('full_name', 'bio', 'contact')

class UpdateArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ('title', 'post',)