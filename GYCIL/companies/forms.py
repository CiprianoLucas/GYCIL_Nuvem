from django import forms
from .models import Company, Category
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from crispy_forms.helper import FormHelper
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class CompanyForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Company
        exclude = ["slug", "enabled", "created_at", "user", "thumbnail"]
        
        
        labels = {
            "company_name": "Rasão social",
            "fantasy_name": "Nome fantasia",
            "representative": "Representante legal",
            "cnpj": "CNPJ",
            "email": "E-mail",
            "zipcode": "Cep",
            "street": "Endereço",
            "number": "Número",
            "city": "Cidade",
            "state": "Estado",
            "phone": "Telefone",
            "logo": "Logomarca",
            "categories": "Categorias",
        }
        
        def save(self, commit=True):
        
            company = super().save(commit=False)
                
            if commit:
                company.save()
            
            return company
        
        def clean(self):
               
            company_email = self.cleaned_data.get('email')
            
            try:
                validate_email(company_email)
            except ValidationError:
                self.add_error('email', ValidationError('Informe um endereço de email válido'))
                
            return super().clean()
        
        def __init__(self, *args, **kwargs):
            super(CompanyForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
              
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

