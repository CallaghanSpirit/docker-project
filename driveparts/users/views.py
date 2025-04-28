from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView,PasswordChangeDoneView, PasswordResetView, PasswordResetConfirmView

from django.views.generic import CreateView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

    # def get_success_url(self):
    #     return reverse('home')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

class ProfileUser(LoginRequiredMixin, UpdateView):
    # model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    def get_success_url(self):
        return reverse_lazy('users:profile')
    
    def get_object(self, queryset = ...):
        return self.request.user
    
class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change.html"

class UserPasswordChangeDone(PasswordChangeDoneView):
    template_name = "users/password_change_done.html"

class UserResetView(PasswordResetView):
    template_name='users/password_reset_form.html'
    email_template_name = "users/password_reset_email.html",
    success_url = reverse_lazy("users:password_reset_done")

class UserPasswordResetConfirm(PasswordResetConfirmView):
    template_name='users/password_reset_confirm.html'
    success_url = reverse_lazy("users:password_reset_complete")
