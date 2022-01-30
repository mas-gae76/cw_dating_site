from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^signup$', RegisterView.as_view(), name='signup'),
    url(r'^login$', UserLoginView.as_view(), name='login'),
    url(r'^logout$', UserLogoutView.as_view(), name='logout'),
    url(r'^$', UserView.as_view(), name='index'),
]