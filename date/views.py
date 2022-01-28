from django.views.generic import ListView
from .models import *
from datetime import datetime


class UserView(ListView):
    model = User
    paginate_by = 50
    queryset = User.objects.exclude(is_staff=True)
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_year'] = datetime.today().year
        return context



