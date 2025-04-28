from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from datetime import date


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    
    class Meta:
        model = get_user_model()
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1','password2', ]
        labels = {
                'first_name':'Имя',
                'last_name':'Фамилия',
                }
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует')
        return email
    
class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True,label='Логин')
    email = forms.EmailField(disabled=True)
    this_year = date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(years=tuple(range(this_year-100, this_year-5))))

    class Meta:
        model = get_user_model()
        fields = ['photo','username', 'email','date_birth', 'first_name', 'last_name']
        labels = {
                'first_name':'Имя',
                'last_name':'Фамилия',
                }
    
class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True}
        ))
    new_password1 = forms.CharField(label='Новый пароль:',widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Подтверждение пароля:',widget=forms.PasswordInput())