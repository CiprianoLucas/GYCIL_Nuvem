from . import views
from django.urls import path

app_name = "services"
urlpatterns = [
    path("", views.index, name="index"),
    path("meus_servicos", views.my_services, name="my_services"),
    path("<int:id>/descricao/", views.descriptions, name = "descriptions"),
    path("procurar/<str:q>", views.search, name="search"),
    path("recusado/<int:id>", views.refuse, name="refuse"),
    path("orcamento/<int:id>", views.budget, name="budget"),
    path("orcamentos_servico/<int:id>", views.budgets_service, name="budgets_service"),
    path("cadastro/", views.create, name="create"),

]
