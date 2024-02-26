from .forms import UserForm, ClientForm
from .models import Client
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserForm, ClientForm


# Create your views here.
def create(request):
    
    
    user = request.user
    
    if user.username:
        if Client.objects.filter(user=user).exists():
            return redirect('companies:index')
        else:
            return redirect('services:index')
    user_type = ""
    
    
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
    'client_form': client_form,
    'user_type': user_type
    }
    
    return render(request, 'clients/create.html', context)
