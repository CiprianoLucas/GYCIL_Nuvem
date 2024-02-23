from django.contrib import admin
from .models import Company, Category
# Register your models here.
@admin.register(Company)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ["id", "fantasy_name","enabled"]
    exclude = ["slug"]
    ordering = ["-id"] # Padrão
    list_filter = ["enabled", "created_at"]
    search_fields = ["fantasy_name"]
    list_display_links = ["fantasy_name"]
    list_editable = ["enabled"]
    list_per_page = 100
    list_max_show_all = 1000
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug","icon"]
    exclude = ["slug"]
    ordering = ["-id"] # Padrão
    list_per_page = 100
    list_max_show_all = 1000