from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Service, Budget
from companies.models import Company
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from .forms import BudgetForm
from django.utils.text import slugify

# Create your views here.

def index(request):
    
    form_action = reverse("services:index")
    services = Service.objects.order_by("-id")
    user_id = request.user.id
    if user_id:
        company = Company.objects.filter(id=user_id)
        categories_company = company.categories

    paginator = Paginator(services, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    for service in page_obj:
        name = service.client.name.split()
        service.client.name = name[0] + " " + name[1][:2] + "***"

    context = {
        "services": page_obj,
        "form_action": form_action
    }

    return render(request, "services/index.html", context)

def search(request, q):
    
    search_value = q
         
    if not search_value:
        return redirect("services:index")
       
    services = Service.objects \
        .filter(Q(id__icontains=search_value) |
                Q(city__icontains=search_value)|
                Q(category__name__icontains=search_value))\
        .order_by("-id")
           
    # Criando o paginator
    paginator = Paginator(services, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = { "services": page_obj }
    
    return render(request, "services/index.html", context)

def refuse(request, id):
    
    company = get_object_or_404(Company, user=request.user)     
    service = get_object_or_404(Service, pk=id)
    
    with transaction.atomic():
        service.companies_refused.add(company)
    service.save()
    
    return redirect("services:index")

def my_services_client(request):
    form_action = reverse("services:my_services_client")
    services = Service.objects.order_by("-id")
    # user_id = request.user.id
    # if user_id:
    #     company = Company.objects.filter(id=user_id)
    #     categories_company = company.categories
    
    paginator = Paginator(services, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "services": page_obj,
        "form_action": form_action
    }

    return render(request, "services/index.html", context)

def my_services_company(request):
    form_action = reverse("services:my_services_company")
    services = Service.objects.order_by("-id")
    user_id = request.user.id
    if user_id:
        company = Company.objects.filter(id=user_id)
        categories_company = company.categories

    paginator = Paginator(services, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "services": page_obj,
        "form_action": form_action
    }

    return render(request, "services/index.html", context)

def budgets_service(request, id):
    service = get_object_or_404(Service, pk=id)
    budgets = Budget.objects.filter(service=service).order_by('-id')
       
    budgets_serialized = [{
        'company': budget.company.fantasy_name,
        'description': budget.description,
        'price': budget.price,
        'date': budget.date,        
    } for budget in budgets]
    
    
    return JsonResponse(budgets_serialized, safe=False)

def descriptions(request, id):
    service = Service.objects.filter(id=id).order_by('-id')
     
    name = service[0].client.name.split()
    new_name = name[0] + " " + name[1][:2] + "***" 
       
    print(new_name)
       
    service_serialized = [{
        'id': str(descriptions.id),
        'street': descriptions.street,
        'description': descriptions.description,
        'cep': descriptions.cep,
        'state': descriptions.state,
        'city': descriptions.city,
        'created_at': str(descriptions.created_at),
        'client': new_name,
        'category': descriptions.category.name,
        'url_refuse': reverse("services:refuse", kwargs={'id': int(descriptions.id)}),
        'url_accept': reverse("services:budget", kwargs={'id': int(descriptions.id)}),
        
    } for descriptions in service]
    
    
    return JsonResponse(service_serialized, safe=False)

def budget(request, id):
    
    company = get_object_or_404(Company, pk=2)     
    service = get_object_or_404(Service, pk=id)
    slug = slugify(f"{service.id}_{company.fantasy_name}")
    
    if not Budget.objects.filter(slug=slug).exists():
        budget = Budget(service=service, company=company)
        budget.save()
        
    budget = get_object_or_404(Budget, slug=slug)     
        
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)

        if form.is_valid():
            budget = form.save()
            budget.status = "Orçamento enviado"
            budget.save()
            messages.success(request, 'Orçamento cadastrado')
            return redirect('services:index')
        
        context = {
        'form': form,
        }
        
        return render(request, 'services/budget.html', context)
            
    
    form = BudgetForm(instance=budget)   
    context = {
    'form': form,
    }
        
    return render(request, 'services/budget.html', context)