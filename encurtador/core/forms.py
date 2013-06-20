from django.forms import ModelForm, EmailField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from core.models import Url


class UrlForm(ModelForm):

    class Meta:
        fields = ('url',)
        model = Url


class UserCreateForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
