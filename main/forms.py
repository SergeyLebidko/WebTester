from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Форма для регистрации нового пользователя
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(strip=True, label='Имя')
    last_name = forms.CharField(strip=True, label='Фамилия')
    email = forms.EmailField(label='Адрес электронной почты')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')
        labels = {'username': 'Логин'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()


# Форма для редактирования данных пользователя
class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(strip=True, label='Имя')
    last_name = forms.CharField(strip=True, label='Фамилия')
    email = forms.EmailField(label='Адрес электронной почты')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {'username': 'Логин'}
