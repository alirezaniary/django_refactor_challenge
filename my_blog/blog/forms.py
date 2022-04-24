from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *


class SignUpForm(UserCreationForm):
	class Meta:
		model = BlogUser
		fields = ('username',
				  'first_name',
				  'last_name',
				  'email',
				  'phone_number',
				  'img_path',
				  'bio',
				  )


class ArticleCreationForm(ModelForm):
	class Meta:
		model = Article
		fields = ('title', 
				  'text',
				  'img_path', 
				  'tag', 
				  'topic', 
				  'is_active',)


class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ('text', 'response_to')


