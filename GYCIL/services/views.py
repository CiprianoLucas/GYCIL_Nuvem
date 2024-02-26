from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Service, Budget
from companies.models import Company
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from .forms import BudgetForm, ServiceForm
from django.utils.text import slugify
from clients.models import Client
from django.conf import settings

# Create your views here.

def index(request):
    
    user = request.user
    if user.username:
        if Client.objects.filter(user=user).exists():
            client = get_object_or_404(Client, user=user) 
            user_type = "client"
            services = Service.objects.filter(client=client)
        else:
            company = get_object_or_404(Company, user=user)
            budgets = Budget.objects.filter(company=company)
            
            user_type = "company"
            services = Service.objects.filter(
                                    Q(city=company.city) &
                                    Q(state=company.state) &
                                    Q(category__in=company.categories.all())
                                      ).exclude(
                                          Q(companies_refused=company) |
                                          Q(id__in=[budget.service.id for budget in budgets])
                                          )
    else:
        return redirect("login:index")
    
    form_action = reverse("services:index")
            
    paginator = Paginator(services, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    for service in page_obj:
        name = service.client.name.split()
        service.client.name = name[0] + " " + name[1][:2] + "***"

    context = {
        "services": page_obj,
        "form_action": form_action,
        "user_type": user_type
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
    
    context = {
        "services": page_obj,
        "user_type": "company"
        }
    
    
    return render(request, "services/index.html", context)

def refuse(request, id):
    
    company = get_object_or_404(Company, user=request.user)     
    service = get_object_or_404(Service, pk=id)
    
    with transaction.atomic():
        service.companies_refused.add(company)
    service.save()
    
    return redirect("services:index")

def my_services(request):
    
    user = request.user
    if user.username:
        if Client.objects.filter(user=user).exists():
            return redirect("services:index")
        else:
            company = get_object_or_404(Company, user=user)
            budgets = Budget.objects.filter(company=company)    
            user_type = "company"
            services = Service.objects.filter(id__in=[budget.service.id for budget in budgets]) \
                                      .exclude(companies_refused=company)
    else:
        return redirect("login:index")
    
    form_action = reverse("services:my_services")
    
    paginator = Paginator(services, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    for service in page_obj:
        name = service.client.name.split()
        service.client.name = name[0] + " " + name[1][:2] + "***"

    context = {
        "services": page_obj,
        "form_action": form_action,
        "user_type": user_type
    }

    return render(request, "services/index.html", context)

def budgets_service(request, id):
    service = get_object_or_404(Service, pk=id)
    budgets = Budget.objects.filter(service=service).order_by('-id')
         
    budgets_serialized = [{
        'company': budget.company.fantasy_name,
        'price': budget.price,
        'date': budget.date,
        'url_accept': reverse("services:accept_budget", kwargs={'id': int(budget.id)}),  
        'url_refuse': reverse("services:refuse_budget", kwargs={'id': int(budget.id)}),
        'budget_file': settings.AWS_S3_CUSTOM_DOMAIN + settings.MEDIA_URL + str(budget.budget_file)
    } for budget in budgets]
    
    
    return JsonResponse(budgets_serialized, safe=False)

def descriptions(request, id):
    service = Service.objects.filter(id=id).order_by('-id')
     
    name = service[0].client.name.split()
    new_name = name[0] + " " + name[1][:2] + "***" 
    
    if service[0].company:
        company=service[0].company.fantasy_name
    else:
        company=""
       
    print(new_name)
       
    service_serialized = [{
        'id': str(descriptions.id),
        'street': descriptions.street,
        'cep': descriptions.cep,
        'state': descriptions.state,
        'city': descriptions.city,
        'created_at': str(descriptions.created_at),
        'description': descriptions.description,
        'client': new_name,
        'status': descriptions.status,
        'date_start': descriptions.date,
        'hours_service': descriptions.hours_service,
        'company': company,
        'price': descriptions.price,
        'category': descriptions.category.name,
        'url_refuse': reverse("services:refuse", kwargs={'id': int(descriptions.id)}),
        'url_accept': reverse("services:budget", kwargs={'id': int(descriptions.id)}),
    } for descriptions in service]
    
    
    return JsonResponse(service_serialized, safe=False)

def budget(request, id):
    
    company = get_object_or_404(Company, user=request.user)     
    service = get_object_or_404(Service, pk=id)
    slug = slugify(f"{service.id}_{company.fantasy_name}")
    
    if not Budget.objects.filter(slug=slug).exists():
        budget = Budget(service=service, company=company)
        budget.save()
        
    budget = get_object_or_404(Budget, slug=slug)     
        
    if request.method == 'POST':
        form = BudgetForm(request.POST, request.FILES, instance=budget)

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
    'user_type': 'company'
    }
        
    return render(request, 'services/budget.html', context)

def refuse_budget(request, id):
    budget = get_object_or_404(Budget, pk=id)
    client = get_object_or_404(Client, user=request.user)
    service = Service.objects.filter(
                                Q(client=client) &
                                Q(id=budget.service.id)).first()
      
    if service.client == client:
        budget.status="Recusado"
        budget.save()
    
    return redirect("services:my_services")

def accept_budget(request, id):
    budget = get_object_or_404(Budget, pk=id)
    client = get_object_or_404(Client, user=request.user)
    service = Service.objects.filter(
                                Q(client=client) &
                                Q(id=budget.service.id)).first()
        
    if service.client == client:
        service.company = budget.company
        service.status = "Serviço em andamento"
        service.price = budget.price
        service.hours_service = budget.hours_service
        service.date = budget.date
        service.save()
        budget.status="Aceito"
        budget.save()
    
    return redirect("services:my_services")

def create(request):
    client = get_object_or_404(Client, user=request.user)
        
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.client = client
            form.save()
            messages.success(request, 'Orçamento cadastrado')
            return redirect('services:index')
        
        context = {
        'form': form,
        'user_type': 'client'
        }
        
        return render(request, 'services/create.html', context)
            
    
    form = ServiceForm(initial={
        'street': client.street,
        'city': client.city,
        'state': client.state,
        'number': client.number,
        'cep': client.zipcode,
        }) 
 
    context = {
    'form': form,
    'user_type': 'client'
    }
        
    return render(request, 'services/create.html', context)