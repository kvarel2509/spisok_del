from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from .models import *


User.__str__ = lambda self: self.first_name
attr_form = {'class': 'form-control', 'aria-describedby': 'addon-wrapping'}


class Otzyv(forms.Form):
    user = forms.CharField(max_length=255, required=True, label='Кто пишет')
    content = forms.CharField(widget=forms.Textarea(), label='Отзыв')
    grade = forms.ChoiceField(choices=(('five', '5'), ('four', '4'), ('free', '3')))


class NewTodo(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['is_to', 'content', 'photo', 'data_deadline']
        widgets = {
            'is_to': forms.Select(attrs=attr_form),
            'content': forms.Textarea(attrs=attr_form),
            'data_deadline': forms.DateTimeInput(attrs=attr_form | {'type': 'datetime-local'}),
            'photo': forms.ClearableFileInput(attrs=attr_form)
        }
        labels = {
            'content': gettext_lazy('Описание задания')
        }

    def clean_is_from(self):
        """Валидатор проверяет, чтобы в поле is_from не было строки abc"""
        is_from = self.cleaned_data['is_from']
        if 'abc' in is_from:
            raise ValidationError('abc содержится в строке')
        return is_from


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=20, label='Логин', widget=forms.TextInput(attrs=attr_form))
    first_name = forms.CharField(max_length=50, label='Имя', widget=forms.TextInput(attrs=attr_form))
    password1 = forms.CharField(label='Пароль', strip=False, widget=forms.PasswordInput(attrs=attr_form))
    password2 = forms.CharField(label='Повторите пароль', strip=False, widget=forms.PasswordInput(attrs=attr_form))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']


class AuthForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs=attr_form))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs=attr_form))

    class Meta:
        model = User
        fields = ['username', 'password']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': 'Новый комментарий'}
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control m-2', 'rows': 3})}


class AccountForm(forms.ModelForm):
    username = forms.CharField(max_length=255, required=False,
                               widget=forms.TextInput(attrs=attr_form | {'disabled': ''}))
    first_name = forms.CharField(max_length=255, required=False,
                                 widget=forms.TextInput(attrs=attr_form | {'disabled': ''}))

    class Meta:
        model = UserInfo
        fields = ['username', 'first_name', 'avatar', 'number', 'mail']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs=attr_form),
            'number': forms.NumberInput(attrs=attr_form | {'type': 'tel'}),
            'mail': forms.EmailInput(attrs=attr_form)
        }


class PasswordEdit(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', strip=False, widget=forms.PasswordInput(attrs=attr_form))
    new_password1 = forms.CharField(label='Новый пароль', strip=False, widget=forms.PasswordInput(attrs=attr_form))
    new_password2 = forms.CharField(label='Повторите пароль', strip=False, widget=forms.PasswordInput(attrs=attr_form))


