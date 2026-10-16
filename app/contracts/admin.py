from django.contrib import admin
from .models import Partner, ContractType, Contract

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'tax_code', 'phone', 'email', 'created_at')
    search_fields = ('code', 'name', 'tax_code')
    list_per_page = 20

@admin.register(ContractType)
class ContractTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'title', 'partner', 'contract_type', 'value', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'contract_type', 'start_date')
    search_fields = ('contract_number', 'title', 'partner__name')
    date_hierarchy = 'created_at'
    list_per_page = 20
