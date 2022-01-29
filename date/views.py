from django.views.generic import ListView
from .models import *
from datetime import datetime
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import RegisterForm
from django.contrib.auth import login
from django.shortcuts import redirect


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
        return redirect('index')
