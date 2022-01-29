from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^signup$', RegisterView.as_view(), name='signup'),
    url(r'^$', UserView.as_view(), name='index'),
]