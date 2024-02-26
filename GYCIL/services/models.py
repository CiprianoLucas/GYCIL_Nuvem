from django.db import models
from django.utils.text import slugify
from companies.models import Company, Category
from clients.models import Client
from django.utils import timezone
class Files(models.Model):
    file = models.FileField(upload_to='services_files/', blank=True, null=True)
class Service(models.Model):
    STATE_CHOICES = {
        "AC": "Acre",
        "AL": "Alagoas",
        "AP": "Amapá",
        "AM": "Amazonas",
        "BA": "Bahia",
        "CE": "Ceará",
        "ES": "Espírito Santo",
        "GO": "Goiás",
        "MA": "Maranhão",
        "MT": "Mato Grosso",
        "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais",
        "PA": "Pará",
        "PB": "Paraíba",
        "PR": "Paraná",
        "PE": "Pernanbuco",
        "PI": "Piauí",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul",
        "RO": "Rondônia",
        "RR": "Roraima",
        "SC": "Santa Catarina",
        "SP": "São Paulo",
        "SE": "Sergipe",
        "TO": "Tocantins",
        "DF": "Distrito Federal",
    }
    
    slug = models.SlugField(unique=True, blank=True)
    street = models.CharField(max_length=255)
    rating = models.CharField(max_length=255, blank=True)
    number = models.CharField(max_length=255, blank=True)
    price = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, default="Aguardando orçamento")
    date = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=3000)
    hours_service = models.CharField(max_length=255, blank=True)
    cep = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    city = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    imagens = models.ImageField(upload_to='services_files/', blank=True, null=True)
    companies_refused = models.ManyToManyField(Company, related_name='refused_services', blank=True)
    
    def save(self, *args, **kwargs):
        super(Service, self).save(*args, **kwargs)
        self.slug = slugify(f'{self.id}_{self.category}')          
        super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}_{self.category}'

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"
        


class Budget(models.Model):
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    slug = models.SlugField(unique=True)
    price = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, default="aguardando orçamento")
    date = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=3000, blank=True)
    hours_service = models.CharField(max_length=255, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.service.id}_{self.company.fantasy_name}')          
        super(Budget, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.service.id}_{self.company.fantasy_name}'

    class Meta:
        verbose_name = "Orçamento"
        verbose_name_plural = "Orçamentos"
        


