from django import forms
from .models import User, Post


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        labels = {
            'email': 'email',
        }


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username']


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['realname', 'location', 'about_me']

    def save(self, commit=True):
        user = super(EditProfileForm, self).save(commit=False)
        return user


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['body']
