from django.shortcuts import render, get_list_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import CompanyForm, UserForm
from django.contrib import messages
from django.db.models import Q
from .models import Company
from clients.models import Client

# Create your views here.
def index(request):
    
    user = request.user
    
    if user.username:
        if Client.objects.filter(user=user).exists():
            # login_user = Client.objects.filter(user=user)
            user_type = "client"
        else:
            return redirect("home")
    else:
        return redirect("home")
    
    companies = Company.objects.order_by("-id")

    # Aplicando a paginação
    paginator = Paginator(companies, 30)
    # /fornecedores?page=1 -> Obtendo a página da URL
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "companies": page_obj,
        "user_type": user_type
        
    }

    return render(request, "companies/index.html", context)


def search(request):
    
    user = request.user
    
    if user.username:
        if Client.objects.filter(user=user).exists():
            # login_user = Client.objects.filter(user=user)
            user_type = "client"
        else:
            user_type = "other"
    else:
        return redirect("login:index")
    
    search_value = str(request.GET.get("q").strip())
       
    if user_type != "client":
        if search_value:
            return redirect(reverse('services:search', kwargs={'q': search_value}))
        else:
            return redirect('services:index')
    
    
    if not search_value:
        return redirect("companies:index")
    
    
    
    companies = Company.objects \
        .filter(Q(fantasy_name__icontains=search_value) |
                Q(city__icontains=search_value)|
                Q(categories__name__icontains=search_value))\
        .order_by("-id")
           
    # Criando o paginator
    paginator = Paginator(companies, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "companies": page_obj,
        "user_type": user_type
        
    }
    
    return render(request, "companies/index.html", context)

def create(request):
    
    user = request.user
    
    if user.username:
        if Company.objects.filter(user=user).exists():
            # login_user = Client.objects.filter(user=user)
            return redirect("clients:index")
        user_type = "client"
    else:
        user_type = ""
       
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        company_form = CompanyForm(request.POST, request.FILES)

        if user_form.is_valid() and company_form.is_valid():
                       
            user = user_form.save()
            client = company_form.save(commit=False)
            client.user = user
            client.save()
            messages.success(request, 'Cliente cadastrado')
            return redirect('companies:index')
        
        context = {
        'user_form': user_form,
        'company_form': company_form
        }
        
        return render(request, 'companies/create.html', context)
            
    
    user_form = UserForm()
    company_form = CompanyForm()
    
    context = {
    'user_form': user_form,
    'company_form': company_form,
    'user_type': user_type
    }
    
    return render(request, 'companies/create.html', context)