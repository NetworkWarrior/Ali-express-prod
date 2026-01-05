from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .models import CustomUser
from .forms import UserRegistrationForm, ProfileUpdateForm
# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html', {'form':UserRegistrationForm()})

    def post(self, request):
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/register.html', {'form':form})


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'login_form':login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in')
            return redirect('landing')
        else:
            return render(request, 'accounts/login.html', {'login_form':login_form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/profile.html', {'user':request.user})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have successfully logged out')
        return redirect('landing')


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        update_form = ProfileUpdateForm(instance=request.user)
        return render(request, 'accounts/update.html', {'update_form':update_form})

    def post(self, request):
        update_form = ProfileUpdateForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )
        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'Updated Successfully!')
            return redirect('accounts:profile')
        return render(request, 'accounts/update.html', {'update_form':update_form})


