from django.urls import path
from . import views

app_name = 'django_single_auth'

urlpatterns = [
    path('login/', views.ServerLogin.as_view(), name='login'),
    path('authenticate/', views.ClientAuthenticate, name='authenticate')
]
