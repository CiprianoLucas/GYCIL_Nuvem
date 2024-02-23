from .forms import UserForm, ClientForm
from .models import Client
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, ClientForm


# Create your views here.
def index(request):
    users = Client.objects.all(). order_by('-id')
    
    context = {
        "users": users
    }
    
    return render(request, 'index.html', context)

def create(request):
       
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        client_form = ClientForm(request.POST, request.FILES)

        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            client = client_form.save(commit=False)
            client.user = user
            client.save()
            messages.success(request, 'Cliente cadastrado')
            return redirect('companies:index')
        
        context = {
        'user_form': user_form,
        'client_form': client_form
        }
        
        return render(request, 'clients/create.html', context)
            
    
    user_form = UserForm()
    client_form = ClientForm()
    
    context = {
    'user_form': user_form,
    'client_form': client_form
    }
    
    return render(request, 'clients/create.html', context)

def login(request):
    return render(request, "clients/login.html")
