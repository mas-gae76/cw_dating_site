from django.views.generic import ListView
from .models import *
from datetime import datetime
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render, reverse


class UserView(ListView):
    model = User
    paginate_by = 50
    template_name = 'index.html'
    queryset = User.objects.exclude(is_staff=True)
    extra_context = {'current_year': datetime.today().year}


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'signup.html'
    extra_context = {'current_year': datetime.today().year}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return render(self.request, 'index.html', context={'user': user})


class UserLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm
    extra_context = {'current_year': datetime.today().year}

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(self.request, email=cd['username'], password=cd['password'])
        login(self.request, user)
        return redirect(reverse('index'))


class DetailUserView(DetailView):
    model = User
    template_name = 'profile.html'


class UserLogoutView(LogoutView):
    next_page = 'index'
