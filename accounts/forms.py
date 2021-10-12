from django import forms
from django.contrib.auth.forms import (UserCreationForm,
                                       PasswordChangeForm, PasswordResetForm,
                                       SetPasswordForm, )

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from accounts.models import Profile
from utils.forms import update_fields_widget
from django.contrib.auth import get_user_model
from allauth.account.forms import LoginForm


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('old_password', 'new_password1', 'new_password2'), 'form-control')


class CustomAuthenticationForm(LoginForm):
    login = forms.CharField(label='Логин или Email', widget=forms.TextInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            update_fields_widget(self, ('login', 'password'), 'form-control')


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(label='Логин', widget=forms.TextInput)
    email = forms.CharField(label='Email', widget=forms.EmailInput)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение', widget=forms.PasswordInput)


class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('email',), 'form-control')


class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('new_password1', 'new_password2',), 'form-control')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'phone', 'country', 'city', 'role') #'__all__'

    avatar = forms.FileField(label='Загрузить аватар', widget=forms.FileInput)
    phone = forms.CharField(label='Телефон', widget=forms.TextInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_fields_widget(self, ('phone','avatar',), 'form-control')

        # сохранить в БД User
        if kwargs['instance']:
            instance = kwargs['instance']
            id = instance.id
            user = User.objects.get(pk=id)
            if len(self.data) > 0:
                yes = False

                if self.data['role']:
                    groupid = self.data['role']
                    group = Group.objects.get(id=groupid)
                    user.groups.clear()
                    user.groups.add(group)
                    yes = True

                if self.data['username']:
                    user.username = self.data['username']
                    yes = True
                if self.data['email']:
                    user.email = self.data['email']
                    yes = True
                if yes:
                    user.save()

        def clean_role(self):
            instance = kwargs['instance']
            id = instance.id
            user = Profile.objects.get(pk=id)
            role = user.role
            introle = str(role)
            if introle != 'Администратор':
               raise forms.ValidationError(f'Менять роль могут только администраторы!')
            return role