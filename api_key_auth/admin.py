from django.contrib import admin
from .models import APIKey
# Register your models here.

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "last_used_at", "revoked")
    search_fields = ("name", )
    readonly_fields = ("hashed_key", "created_at", "last_used_at")
    