from django.urls import path

from . import views 

app_name = 'main'  # Define a namespace for URL routing

urlpatterns = [
    path('', views.home, name='home'),
]
