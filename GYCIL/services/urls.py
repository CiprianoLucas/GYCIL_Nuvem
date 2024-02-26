from . import views
from django.urls import path

app_name = "services"
urlpatterns = [
    path("", views.index, name="index"),
    path("meus_servicos", views.my_services, name="my_services"),
    path("<int:id>/descricao/", views.descriptions, name = "descriptions"),
    path("procurar/<str:q>", views.search, name="search"),
    path("orcamentos_servico/<int:id>", views.budgets_service, name="budgets_service"),
    path("cadastro/", views.create, name="create"),
    path("aceitar_orcamento/<int:id>", views.accept_budget, name="accept_budget"),
    path("recusar_orcamento/<int:id>", views.refuse_budget, name="refuse_budget"),
    path("orcamento/<int:id>", views.budget, name="budget"),
    path("recusado/<int:id>", views.refuse, name="refuse"),
    
]
