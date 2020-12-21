from django.urls import path
from . import views

urlpatterns = [
    path('listen/', views.incoming_message, name='webhook_message')
]

app_name = 'api'