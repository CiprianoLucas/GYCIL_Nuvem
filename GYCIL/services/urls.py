from . import views
from django.urls import path

app_name = "services"
urlpatterns = [
    path("", views.index, name="index"),
    path("cliente", views.my_services_client, name="my_services_client"),
    path("empresa", views.my_services_company, name="my_services_company"),
    path("<int:id>/descricao/", views.descriptions, name = "descriptions"),
    path("procurar/<str:q>", views.search, name="search"),
    path("recusado/<int:id>", views.refuse, name="refuse"),
    path("orcamento/<int:id>", views.budget, name="budget"),
    path("orcamentos_servico/<int:id>", views.budgets_service, name="budgets_service"),

]
