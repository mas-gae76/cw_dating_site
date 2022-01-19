from django.views.generic import ListView
from .models import *


class UserView(ListView):
    model = User
    paginate_by = 50
    queryset = User.objects.exclude(is_staff=True)
    template_name = 'index.html'


