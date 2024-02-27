from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from PIL import Image
import os
from django.core.files.base import ContentFile
from io import BytesIO


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.ImageField(upload_to="icons_categories", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
class Company(models.Model):
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
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="0")
    fantasy_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    representative = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, unique=True)
    zipcode = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    phone = models.CharField(max_length=20)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    logo = models.ImageField(upload_to="companies_logos", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="companies_logo_thumb", blank=True, null=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.fantasy_name
        
    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.fantasy_name}_{self.user.id}")
                          
        super(Company, self).save(*args, **kwargs)

        # Criando a thumbnail
        self.__create_thumbnail()
        super(Company, self).save(*args, **kwargs)
        
    def __create_thumbnail(self):
        if not self.logo:
            return

        logo = Image.open(self.logo)
        size = (30, 30)
        logo.thumbnail(size)

        thumb_io = BytesIO()
        logo.save(thumb_io, logo.format, quality=85)
        extension = f".{logo.format.lower()}"


        self.thumbnail.save(f'{self.slug}_thumb{extension}', ContentFile(
            thumb_io.getvalue()), save=False)

    def __delete_file_if_exists(self, file):
        if file and os.path.isfile(file.path):
            os.remove(file.path)

    def delete(self, *args, **kwargs):
        self.__delete_file_if_exists(self.logo)
        self.__delete_file_if_exists(self.thumbnail)
        super(Company, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        

