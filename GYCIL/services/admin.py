from django.contrib import admin
from .models import Service
# Register your models here.
@admin.register(Service)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["id","cep", "created_at" ,"client", "company" ,"category"]
    exclude = ["slug"]
    ordering = ["-id"]
    list_filter = ["created_at"]
    search_fields = ["cep","client","company" ,"category"]
    list_display_links = ["id"]
    list_per_page = 100
    list_max_show_all = 1000
