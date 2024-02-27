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
            "budget_file": "Arquivo de orçamento",
            "hours_service": "Horas de serviço",
        }
        
        def save(self, commit=True):
        
            budget = super().save(commit=False)
                
            if commit:
                budget.save()
            
            return budget
        

class FinishForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["nfe", "nfse"]
        
        
        labels = {
            "nfe": "Nota Fiscal de Produto",
            "nfse": "Nota Fiscal de Serviço",
        }
        
    def clean(self):
        cleaned_data = super().clean()
        nfe = self.cleaned_data.get('nfe',"")
        nfse = self.cleaned_data.get('nfse',"")

        if not nfe and not nfse:
            raise ValidationError('Pelo menos um dos campos deve ser preenchido.')
        
        return cleaned_data
    
    def save(self, commit=True):
    
        service = super().save(commit=False)
            
        if commit:
            service.save()
        
        return service
            
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude = ["slug", "rating", "price", "status", "date", "hours_service", "created_at", "client", "company", "companies_refused", "nfe", "nfse"]
        
        
        labels = {
            "category": "Categoria",
            "description": "Descrição",
            "street": "Endereço",
            "cep": "CEP",
            "state": "Estado",
            "city": "Cidade",
            "number": "Número",
            "imagem": "Imagem",
        }
        
        def save(self, commit=True):
        
            service = super().save(commit=False)
                
            if commit:
                service.save()
            
            return service