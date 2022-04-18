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
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class UserView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 50
    template_name = 'index.html'
    extra_context = {'current_year': datetime.today().year}
    login_url = 'login'

    def get_queryset(self):
        if 'users' in cache:
            users = cache.get('users').exclude(id=self.request.user.id)
            return users
        else:
            results = User.objects.annotate(average_rating=Avg('ratings__rating')).exclude(is_staff=True)
            cache.set('users', results, timeout=settings.CACHE_TTL)
            return results.exclude(id=self.request.user.id)


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

    def get_context_data(self, **kwargs):
        context = super(DetailUserView, self).get_context_data(**kwargs)
        context['current_year'] = datetime.today().year

        today = date.today()
        user_birthday = context['user'].birthday
        context['age'] = today.year - user_birthday.year - ((today.month, today.day) < (user_birthday.month, user_birthday.day))

        current_user = context['user'].id
        rating_user_db = Rating.objects.filter(sender__id=self.request.user.id, user__id=current_user)

        context['is_sympathized'] = Sympathy.objects.filter(who=self.request.user, whom__id=current_user)

        if len(rating_user_db) == 0:
            context['is_review'] = True
        else:
            context['is_review'] = False
        return context


class UserLogoutView(LogoutView):
    next_page = 'login'


@login_required
def rate_user(request, pk):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        rating_value = request.POST.get('rating_value')
        rating = Rating(user_id=user_id, rating=rating_value, sender=request.user)
        rating.save()
        return JsonResponse({'result': True})


@login_required
def sympathize(request, pk):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        sympathy = True if request.POST.get('sympathize') == "true" else False
        existing_1 = Sympathy.objects.filter(whom__id=user_id, who=request.user)
        existing_2 = Sympathy.objects.filter(whom=request.user, who__id=user_id)

        if len(existing_1) != 0:
            matching_1 = existing_1.values('matching')[0]['matching']
            process_sympathy(existing_1, matching_1, sympathy)

        elif len(existing_2) != 0:
            matching_2 = existing_2.values('matching')[0]['matching']
            process_sympathy(existing_2, matching_2, sympathy)
        else:
            Sympathy.objects.create(who=request.user, whom_id=user_id)

        return JsonResponse({'result': sympathy})


def process_sympathy(obj, matching, sympathy):
    if not matching and not sympathy:
        obj.delete()
    else:
        obj.update(matching=sympathy)
