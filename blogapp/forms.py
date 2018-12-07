from django import forms
from .models import article, author, comment, category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class articleForm(forms.ModelForm):    
    class Meta:
        model = article
        fields = ['title', 'body', 'image', 'category']


class authorForm(forms.ModelForm):    
    class Meta:
        model = author
        fields = ['profile_picture', 'details']

class registerForm(UserCreationForm):    
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']

class commentForm(forms.ModelForm):    
    class Meta:
        model = comment
        fields = ['name', 'email', 'post_comment']

class categoryForm(forms.ModelForm):    
    class Meta:
        model = category
        fields = ['name']

