from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from PIL import Image
import os
from django.core.files.base import ContentFile
from io import BytesIO
# Create your models here.
class Client(models.Model):
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

    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length=255, default="Sem nome")
    slug = models.SlugField(unique=True, blank=True)
    cpf = models.CharField(max_length=20, unique=True)
    zipcode = models.CharField(max_length=20)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to="photos_clients", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="thumb_clients", blank=True, null=True)

    def __str__(self):
        return self.name

       
    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.name}_{self.user}')
                       
        super(Client, self).save(*args, **kwargs)

        # Criando a thumbnail
        self.__create_thumbnail()
        super(Client, self).save(*args, **kwargs)
        
    def __create_thumbnail(self):
        if not self.photo:
            return

        photo = Image.open(self.photo)
        size = (30, 30)
        photo.thumbnail(size)

        thumb_io = BytesIO()
        photo.save(thumb_io, photo.format, quality=85)
        extension = f".{photo.format.lower()}"
        


        self.thumbnail.save(f'{self.slug}_thumb{extension}', ContentFile(
            thumb_io.getvalue()), save=False)

    def __delete_file_if_exists(self, file):
        if file and os.path.isfile(file.path):
            os.remove(file.path)

    def delete(self, *args, **kwargs):
        self.__delete_file_if_exists(self.photo)
        self.__delete_file_if_exists(self.thumbnail)
        super(Client, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
