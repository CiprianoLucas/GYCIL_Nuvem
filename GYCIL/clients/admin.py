from django.contrib import admin
from .models import Client
# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["id","name"]
    exclude = ["slug"]
    ordering = ["-id"]
    list_filter = ["created_at"]
    search_fields = ["name"]
    list_display_links = ["name"]
    list_per_page = 100
    list_max_show_all = 1000
    