from django import forms
from .models import Budget, Service
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        exclude = ["slug", "status", "company", "service"]
        
        
        labels = {
            "price": "Valor final",
            "date": "Data de inicio",
            "description": "Descrição",
            "hours_service": "Horas de serviço",
        }
        
        def save(self, commit=True):
        
            budget = super().save(commit=False)
                
            if commit:
                budget.save()
            
            return budget
        
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ["slug", "rating", "price", "status", "date", "hours_service", "created_at", "client", "company", "companies_refused"]
        
        
        labels = {
            "category": "Categoria",
            "description": "Descrição",
            "street": "Endereço",
            "cep": "CEP",
            "state": "Estado",
            "city": "Cidade",
            "number": "Número",
            "imagens": "Imagem",
        }
        
        def save(self, commit=True):
        
            service = super().save(commit=False)
                
            if commit:
                service.save()
            
            return service