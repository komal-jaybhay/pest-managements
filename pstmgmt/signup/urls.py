from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.login, name='role_login'),
    path('authenticateUser', views.authenticateUser, name='authenticateUser'),
    ]

app_name = 'signup'