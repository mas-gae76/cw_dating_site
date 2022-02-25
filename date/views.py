from django.views.generic import ListView
from .models import *
from datetime import datetime
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render, reverse
from django.conf import settings
from django.core.cache import cache
from django.db.models import Avg


# TODO: удаление/обновление кэша при удалении/обновлении объекта БД


class UserView(ListView):
    model = User
    paginate_by = 50
    template_name = 'index.html'
    extra_context = {'current_year': datetime.today().year}

    def get_queryset(self):
        if 'users' in cache:
            users = cache.get('users')
            return users
        else:
            results = User.objects.annotate(average_rating=Avg('ratings__rating')).exclude(is_staff=True)
            cache.set('users', results, timeout=settings.CACHE_TTL)
            return results


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

    def get_queryset(self):
        return cache.get('users').filter(id=self.kwargs['pk'])


class UserLogoutView(LogoutView):
    next_page = 'index'


def rate_user(request, pk):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        rating_value = request.POST.get('rating_value')
        Rating.objects.create(user=User.objects.get(id=user_id), rating=rating_value, sender=request.user)
        return redirect('profile')
