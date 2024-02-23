from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import UserForm
# Create your views here.
def index(request):
    users = User.objects.all(). order_by('-id')
    
    context = {
        "users": users
    }
    
    return render(request, 'index.html', context)

def create(request):
    
    form = UserForm()
    
    context = {
        "form": form
    }
    
    return render(request, "users/create.html", context)

def login(request):
    return render(request, "users/login.html")

def logout(request):
    return render(request, "users/logout.html")

def update(request, username):
    return render(request, "users/update.html")

