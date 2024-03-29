from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Service, Budget
from companies.models import Company
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from .forms import BudgetForm, ServiceForm, FinishForm
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
            services = Service.objects.filter(client=client).exclude(Q(status="Cancelado"))
        else:
            company = get_object_or_404(Company, user=user)
            budgets = Budget.objects.filter(company=company)
            
            user_type = "company"
            services = Service.objects.filter(
                                    Q(city=company.city) &
                                    Q(state=company.state) &
                                    Q(category__in=company.categories.all()) &
                                    Q(company=None)
                                      ).exclude(
                                          Q(companies_refused=company) |
                                          Q(id__in=[budget.service.id for budget in budgets])|
                                          Q(status="Cancelado"))
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
    
    company = get_object_or_404(Company, user=request.user)
    budgets = Budget.objects.filter(company=company)
       
    services = Service.objects \
        .filter((Q(id__icontains=search_value) |
                Q(city__icontains=search_value)|
                Q(category__name__icontains=search_value)) &
                Q(company=None)
                ).exclude(  Q(status="Cancelado")|
                            Q(companies_refused=company) |
                            Q(id__in=[budget.service.id for budget in budgets])|
                            Q(status="Cancelado"))

        
           
    # Criando o paginator
    paginator = Paginator(services, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    for service in page_obj:
        name = service.client.name.split()
        service.client.name = name[0] + " " + name[1][:2] + "***"
    
    
    context = {
        "services": page_obj,
        "user_type": "company"
        }
    
    
    return render(request, "services/index.html", context)

def refuse(request, id):
    
    company = get_object_or_404(Company, user=request.user)     
    service = get_object_or_404(Service, pk=id)
    if Budget.objects.filter(service=service).exists():
        budget = get_object_or_404(Budget, service=service)
        budget.status="Cancelado"
        budget.save()
    
    with transaction.atomic():
        service.companies_refused.add(company)
    service.save()
    
    return redirect("services:index")

def delete(request, id):
    service = get_object_or_404(Service, pk=id)
    client = get_object_or_404(Client, user=request.user)
     
    if service.client == client:
        service.status="Cancelado"
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
            services = Service.objects.filter( (Q(company=company) |
                                               Q(company=None)) &
                                               Q(id__in=[budget.service.id for budget in budgets])
                                              ).exclude(Q(companies_refused=company) |
                                                        Q(status="Cancelado"))
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
    budgets = Budget.objects.filter(service=service).exclude(status=["Recusado","Cancelado"])
    
    filter_budgets_empty = [budget for budget in budgets if budget.price != ""]
    filter_budgets_not_accept = [budget for budget in filter_budgets_empty if budget.status != "Recusado"]
            
         
    budgets_serialized = [{
        'company': budget.company.fantasy_name,
        'price': budget.price,
        'date': budget.date,
        'url_accept': reverse("services:accept_budget", kwargs={'id': int(budget.id)}),  
        'url_refuse': reverse("services:refuse_budget", kwargs={'id': int(budget.id)}),
        'budget_file': settings.MEDIA_URL + str(budget.budget_file)
    } for budget in filter_budgets_not_accept]
    
    
    return JsonResponse(budgets_serialized, safe=False)

def descriptions(request, id):
    service = Service.objects.filter(id=id).order_by('-id')
     
    name = service[0].client.name.split()
    new_name = name[0] + " " + name[1][:2] + "***" 
    
    if service[0].company:
        company=service[0].company.fantasy_name
    else:
        company=""
        
    user = request.user
    if user.username:
        if Client.objects.filter(user=user).exists():
            status = service[0].status
        else:
            company_user = get_object_or_404(Company, user=request.user)
            
            if Budget.objects.filter(Q(service=service[0]) &
                                     Q(company=company_user)).exists(): 
                
                budget = get_object_or_404(Budget, Q(service=service[0]) &
                                                   Q(company=company_user))
                status = budget.status
                
            else:
                status = service[0].status
                
    print(service[0].status)
    print(status)
    
    if status == "Aceito":
        if service[0].status == "Serviço em andamento":
            url_accept = reverse("services:finish", kwargs={'id': int(service[0].id)})
        else:
            url_accept = ""
            status = service[0].status
    else:
        url_accept = reverse("services:budget", kwargs={'id': int(service[0].id)})
             
    service_serialized = [{
        'id': str(descriptions.id),
        'street': descriptions.street,
        'cep': descriptions.cep,
        'state': descriptions.state,
        'city': descriptions.city,
        'created_at': str(descriptions.created_at),
        'description': descriptions.description,
        'client': new_name,
        'status': status,
        'date_start': descriptions.date,
        'hours_service': descriptions.hours_service,
        'company': company,
        'price': descriptions.price,
        'category': descriptions.category.name,
        'url_refuse': reverse("services:refuse", kwargs={'id': int(descriptions.id)}),
        'url_accept': url_accept,
        'url_delete': reverse("services:delete", kwargs={'id': int(descriptions.id)}),
    } for descriptions in service]
    
    
    return JsonResponse(service_serialized, safe=False)

def finish(request, id):
    company = get_object_or_404(Company, user=request.user)
    service = get_object_or_404(Service, pk=id)
    
    if not service.company == company:
       return redirect ("services:index") 
   
    if request.method == 'POST':
        form = FinishForm(request.POST, request.FILES, instance=service)

        if form.is_valid():
            form.clean()
            service = form.save()
            service.status = "Concluido"
            print(service.status)
            service.save()
            return redirect('services:index')
        
        
        form = FinishForm(instance=service)
        context = {
        'form': form,
        'user_type': 'company'
        }
        messages.error(request, "Falha ao finalizar. Deve ter ao menos uma Nota Fiscal.")
        
        return render(request, 'services/finish.html', context)
            
    
    form = FinishForm(instance=service)   
    context = {
    'form': form,
    'user_type': 'company'
    }
        
    return render(request, 'services/finish.html', context)


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
        'user_type': 'company'
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


def create_company(request, id):
    client = get_object_or_404(Client, user=request.user)
    company = get_object_or_404(Company, pk=id)
    
        
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.client = client
            form.instance.company = company
            service = form.save()
            budget = Budget(service=service, company=company)
            budget.save()
            
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