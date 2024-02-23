from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path("", views.index, name="index"),
    path("cadastro/", views.create, name="create"),
    path("login/", views.login, name="login"),
    path("usuarios/<str:username/", views.update, name="update"),
]
