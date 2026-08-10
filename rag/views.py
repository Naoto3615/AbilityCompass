from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services import (
    generate_rag_advice_for_child,
    generate_rag_advice_for_user,
    embed_support_record,
)
from daycare.models import Child, SupportRecord


@login_required
def rag_advice_staff(request, child_id):
    """支援員向け: 児童の個別AIアドバイス"""
    if not hasattr(request.user, 'staff_profile'):
        return redirect('/')

    child = get_object_or_404(Child, id=child_id)

    advice_result = None
    query = ''

    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        if query:
            advice_result = generate_rag_advice_for_child(child, query)

    total_records = SupportRecord.objects.filter(child=child).count()
    embedded_records = SupportRecord.objects.filter(
        child=child, embedding__isnull=False
    ).count()

    return render(request, 'rag/advice_staff.html', {
        'child': child,
        'advice_result': advice_result,
        'query': query,
        'total_records': total_records,
        'embedded_records': embedded_records,
    })


@login_required
def rag_advice_user(request):
    """利用者向け: 自分の特性AIアドバイス"""
    if not hasattr(request.user, 'user_profile'):
        return redirect('/')

    profile = request.user.user_profile
    advice_result = None
    query = ''

    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        if query:
            advice_result = generate_rag_advice_for_user(profile, query)

    from daily.models import DailyRecord
    record_count = DailyRecord.objects.filter(user=request.user).count()

    return render(request, 'rag/advice_user.html', {
        'profile': profile,
        'advice_result': advice_result,
        'query': query,
        'record_count': record_count,
    })


@login_required
@require_POST
def embed_records(request, child_id):
    """支援記録を埋め込む（支援員専用管理機能）"""
    if not hasattr(request.user, 'staff_profile'):
        return JsonResponse({'error': 'forbidden'}, status=403)

    child = get_object_or_404(Child, id=child_id)
    records = SupportRecord.objects.filter(child=child)
    success_count = 0
    for record in records:
        if embed_support_record(record):
            success_count += 1

    return JsonResponse({'success': success_count, 'total': records.count()})
