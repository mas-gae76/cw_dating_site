from django.conf.urls import url
from django.urls import path
from .views import *


urlpatterns = [
    url(r'^signup$', RegisterView.as_view(), name='signup'),
    url(r'^login$', UserLoginView.as_view(), name='login'),
    url(r'^logout$', UserLogoutView.as_view(), name='logout'),
    url(r'^$', UserView.as_view(), name='index'),
    path('profile/<uuid:pk>', DetailUserView.as_view(), name='profile'),
    path('profile/<uuid:pk>/rate', rate_user, name='rate'),
    path('profile/<uuid:pk>/sympathize', sympathize, name='sympathize'),
]