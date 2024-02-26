from django.urls import path
from . import views

app_name = "login"
urlpatterns = [
    path('', views.login, name='index'),
    path('logout/', views.logout, name='logout'),
     
]