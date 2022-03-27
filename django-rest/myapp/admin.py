from django.contrib import admin
from .models import Cost
from .models import Attachment
from .models import PasswordReset
from .models import MyConfig
from .models import VendorSubsidiary
from .models import Product
from .models import Channel
from .models import Price
from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin

class CostResource(resources.ModelResource):
    class Meta:
        model = Cost

class VendorSubsidiaryResource(resources.ModelResource):
    class Meta:
        model = VendorSubsidiary

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product

# Register your models here.
@admin.register(Cost)
class CostAdmin(ExportActionMixin, admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', 'last_updated_by')
    resource_class = CostResource

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

@admin.register(MyConfig)
class MyConfigAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

@admin.register(VendorSubsidiary)
class VendorSubsidiaryAdmin(ImportExportModelAdmin):
    resource_class = VendorSubsidiaryResource

@admin.register(Product)
class VendorSubsidiaryAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
