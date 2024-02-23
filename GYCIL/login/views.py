from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.http import HttpResponse

class UserLoginView(View):
    template_name = "auth/loginUser.html"
    next_page = 'companies:index'
    redirect_authenticated_user = True

    def get(self, request):
        error_message = None
        return self.mostrar_pagina_login_user(request, error_message)

    def post(self, request):
        email_user = request.POST.get('email_user')
        password_user = request.POST.get('password_user')
        user = authenticate(request, email_user=email_user, password_user=password_user)
        
        if user is not None:
            login(request, user)
            return redirect('companies:index')
        else:
            error_message = "Email ou senha incorretos. Por favor, tente novamente."
            return self.mostrar_pagina_login_user(request, error_message)

    def mostrar_pagina_login_user(self, request, error_message=None):
        return render(request, self.template_name, {'error_message': error_message})


class CompanyLoginView(View):
    template_name = "auth/loginCompany.html"
    next_page = 'companies:index'

    def get(self, request):
        error_message = None
        return self.mostrar_pagina_login_company(request, error_message)

    def post(self, request):
        email_company = request.POST.get('email_company')
        cnpj = request.POST.get('cnpj')
        password_company = request.POST.get('password_company')
        company = authenticate(request, email_company=email_company, cnpj=cnpj, password_company=password_company)

        if company is not None:
            login(request, company)
            return HttpResponse('Login realizado com sucesso!')
        else:
            error_message = "Email ou senha incorretos. Por favor, tente novamente."
            return self.mostrar_pagina_login_company(request, error_message)

    def mostrar_pagina_login_company(self, request, error_message=None):
        return render(request, self.template_name, {'error_message': error_message})
