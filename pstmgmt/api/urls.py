from django.urls import path
from . import views

urlpatterns = [
    path('listen/', views.incoming_message, name='webhook_message'),
    path('listen1/', views.incoming_Q_message, name='webhook_Q_message')
]

app_name = 'api'