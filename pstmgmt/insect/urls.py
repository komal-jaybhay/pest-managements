from django.urls import path
from . import views
from django.views.generic import RedirectView
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dashboard', views.dashboard, name='insect_dashboard'),
    path('add', views.add, name='add_insect'),
    path('add_new_insect', views.add_new_insect, name='add_new_insect'),
    path('view', views.viewDetails, name='view_insect'),
    ]

app_name = 'insect'