from django.shortcuts import render
from django.db.models import Sum, Count
from .models import Contract, Partner, ContractType

def home_view(request):
    """
    Homepage view for Đề 34: Hệ thống Quản lý Hợp đồng.
    """
    total_contracts = Contract.objects.count()
    total_partners = Partner.objects.count()
    active_contracts = Contract.objects.filter(status='ACTIVE').count()
    draft_contracts = Contract.objects.filter(status='DRAFT').count()
    completed_contracts = Contract.objects.filter(status='COMPLETED').count()
    total_value = Contract.objects.aggregate(total=Sum('value'))['total'] or 0

    recent_contracts = Contract.objects.select_related('partner', 'contract_type')[:10]

    context = {
        'page_title': 'Hệ thống Quản lý Hợp đồng',
        'total_contracts': total_contracts,
        'total_partners': total_partners,
        'active_contracts': active_contracts,
        'draft_contracts': draft_contracts,
        'completed_contracts': completed_contracts,
        'total_value': total_value,
        'recent_contracts': recent_contracts,
        'is_secure': request.is_secure(),
    }
    return render(request, 'contracts/index.html', context)
