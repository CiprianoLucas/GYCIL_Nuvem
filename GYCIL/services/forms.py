from django import forms
from .models import Budget
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
        