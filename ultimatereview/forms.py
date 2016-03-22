from django import forms
from ultimatereview.models import Researcher, Review, Query, Paper, UserProfile
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

class UpdateProfileForm(forms.ModelForm):

    username = forms.CharField(label='Username')
    email = forms.CharField(label='Email')
    password = forms.CharField(label = 'Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class CreateReviewForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Must be unique'}))
    class Meta:
        model = Review
        fields = ('title',)

class CreateSimpleQueryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Must be unique'}))
    class Meta:
        model = Query
        fields = ('name',)
