from django.contrib import admin
from .models import Cost
from .models import Attachment
from .models import PasswordReset
from .models import MyConfig

# Register your models here.
@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'last_updated_by')

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

@admin.register(MyConfig)
class MyConfigAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
