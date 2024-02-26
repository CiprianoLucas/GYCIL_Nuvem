from django.shortcuts import render, get_list_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from clients.models import Client
def home(request):
    user = request.user
    
    if user.username:
        if Client.objects.filter(user=user).exists():
            # login_user = Client.objects.filter(user=user)
            user_type = "client"
        else:
            user_type = "company"
    else:
        user_type = ""
    
    context = {
        "user_type": user_type
    }
    
    
    return render(request, 'home.html', context)