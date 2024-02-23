from django import forms
from .models import Client
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ["slug", "enabled", "created_at", "user", "thumbnail"]
        
        
        labels = {
            "name": "Nome completo",
            "cpf": "CPF",
            "zipcode": "Cep",
            "street": "Endereço",
            "number": "Número",
            "city": "Cidade",
            "state": "Estado",
            "phone": "Telefone",
            "photo": "Foto de usuario",
        }
        
        error_messages = {
            "name": {
                "required": "O campo nome é obrigatório",
                "unique": "Já existe um produto cadastrado com esse nome"
            },
            "cpf": {
                "required": "O campo descrição é obrigatório",                
            },
        }
        
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type":"date"}, format="%Y-%m-%d")
        }
        
        def save(self, commit=True):
        
            client = super().save(commit=False)
                
            if commit:
                client.save()
            
            return client
        
        def clean(self):
               
            client_email = self.cleaned_data.get('email')
            
            try:
                validate_email(client_email)
            except ValidationError:
                self.add_error('email', ValidationError('Informe um endereço de email válido'))
                
            return super().clean()
            
        
       
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
        
        
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        
    def save(self, commit=True):
        password = self.cleaned_data.get('password')
        
        user = super().save(commit=False)
        
        if password:
            user.set_password(password)
            
        if commit:
            user.save()
            
        return user
    

        
        