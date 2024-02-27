from django.urls import path
from . import views

app_name = "companies"
urlpatterns = [
    path("", views.index, name="index"),
    path("cadastro/", views.create, name="create"),
    path("procurar/", views.search, name="search"),
    path("procurar/<str:q>", views.search_q, name="search_q"),
]
