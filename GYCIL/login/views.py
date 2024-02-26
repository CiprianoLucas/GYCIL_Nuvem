from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth

def login(request):
    
    user = request.user
    
    if user.username:
        auth.logout(request)
    
    form = AuthenticationForm(request)
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            
            return redirect("companies:index")
    
    
    context = {
        'form': form,
    }
    
    return render(request, "auth/login.html", context)

def logout(request):
    auth.logout(request)
    return redirect("home")