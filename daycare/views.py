import datetime
import json

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AddParentForm, ChildForm, DevelopmentScoreForm, SupportRecordForm
from .models import (
    Child,
    DevelopmentScore,
    ParentChildLink,
    ParentProfile,
    StaffChildLink,
    StaffProfile,
    SupportRecord,
)


def get_staff_or_403(request):
    try:
        return request.user.staff_profile
    except Exception:
        raise PermissionDenied


def get_parent_or_403(request):
    try:
        return request.user.parent_profile
    except Exception:
        raise PermissionDenied


# ─── 支援員向けビュー ─────────────────────────────────────────────────────────

@login_required
def staff_dashboard(request):
    staff = get_staff_or_403(request)
    links = StaffChildLink.objects.filter(staff=staff).select_related('child')

    today = datetime.date.today()
    children_data = []
    for link in links:
        child = link.child
        latest = SupportRecord.objects.filter(child=child).order_by('-date').first()
        recorded_today = SupportRecord.objects.filter(child=child, date=today).exists()
        children_data.append({
            'child': child,
            'latest_record': latest,
            'recorded_today': recorded_today,
        })

    return render(request, 'daycare/staff_dashboard.html', {
        'children_data': children_data,
    })


@login_required
def child_add(request):
    """既存の児童を担当に追加する（新規作成ではない）"""
    staff = get_staff_or_403(request)

    linked_child_ids = StaffChildLink.objects.filter(staff=staff).values_list('child_id', flat=True)
    available_children = Child.objects.exclude(id__in=linked_child_ids).order_by('nickname')

    if request.method == 'POST':
        child_id = request.POST.get('child_id')
        if child_id:
            try:
                child = Child.objects.get(id=child_id)
                link, created = StaffChildLink.objects.get_or_create(staff=staff, child=child)
                if created:
                    messages.success(request, f'{child.nickname}さんを担当に追加しました。')
                else:
                    messages.info(request, 'すでに担当登録済みです。')
            except Child.DoesNotExist:
                messages.error(request, '児童が見つかりません。')
        else:
            messages.error(request, '児童を選択してください。')
        return redirect('daycare:staff_dashboard')

    return render(request, 'daycare/child_add.html', {
        'available_children': available_children,
    })


@login_required
def child_detail(request, child_id):
    staff = get_staff_or_403(request)
    child = get_object_or_404(Child, id=child_id)
    if not StaffChildLink.objects.filter(staff=staff, child=child).exists():
        raise PermissionDenied

    records = SupportRecord.objects.filter(child=child)
    parent_links = ParentChildLink.objects.filter(child=child).select_related('parent__user')

    return render(request, 'daycare/child_detail.html', {
        'child': child,
        'records': records,
        'parent_links': parent_links,
    })


@login_required
def record_add(request, child_id):
    staff = get_staff_or_403(request)
    child = get_object_or_404(Child, id=child_id)
    if not StaffChildLink.objects.filter(staff=staff, child=child).exists():
        raise PermissionDenied

    if request.method == 'POST':
        form = SupportRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.child = child
            record.author = request.user
            record.save()
            messages.success(request, '支援記録を保存しました。')
            return redirect('daycare:child_detail', child_id=child.id)
    else:
        form = SupportRecordForm(initial={'date': datetime.date.today()})

    return render(request, 'daycare/record_form.html', {
        'form': form,
        'child': child,
    })


@login_required
def add_parent_to_child(request, child_id):
    staff = get_staff_or_403(request)
    child = get_object_or_404(Child, id=child_id)
    if not StaffChildLink.objects.filter(staff=staff, child=child).exists():
        raise PermissionDenied

    all_parents = ParentProfile.objects.select_related('user').order_by('user__username')
    linked_parent_ids = ParentChildLink.objects.filter(child=child).values_list('parent_id', flat=True)
    available_parents = all_parents.exclude(id__in=linked_parent_ids)

    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        if parent_id:
            try:
                parent_profile = ParentProfile.objects.get(id=parent_id)
                link, created = ParentChildLink.objects.get_or_create(parent=parent_profile, child=child)
                if created:
                    messages.success(request, f'{parent_profile.user.username}さんを{child.nickname}の保護者として登録しました。')
                else:
                    messages.info(request, 'すでに紐付け済みです。')
            except ParentProfile.DoesNotExist:
                messages.error(request, '保護者が見つかりません。')
        else:
            messages.error(request, '保護者を選択してください。')
        return redirect('daycare:child_detail', child_id=child.id)

    return render(request, 'daycare/add_parent.html', {
        'child': child,
        'available_parents': available_parents,
    })


# ─── 保護者向けビュー ─────────────────────────────────────────────────────────

@login_required
def parent_dashboard(request):
    parent = get_parent_or_403(request)
    links = ParentChildLink.objects.filter(parent=parent).select_related('child')

    children_data = []
    for link in links:
        child = link.child
        shared_records = SupportRecord.objects.filter(
            child=child, share_with_parent=True
        ).order_by('-date')[:10]
        children_data.append({
            'child': child,
            'records': shared_records,
        })

    return render(request, 'daycare/parent_dashboard.html', {
        'children_data': children_data,
    })


# ─── サインアップ ─────────────────────────────────────────────────────────────

def staff_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            StaffProfile.objects.create(user=user)
            login(request, user)
            return redirect('daycare:staff_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'daycare/signup.html', {'form': form, 'role': '支援員'})


def parent_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            ParentProfile.objects.create(user=user)
            login(request, user)
            return redirect('daycare:parent_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'daycare/signup.html', {'form': form, 'role': '保護者'})


# ─── 発達スコア ───────────────────────────────────────────────────────────────

@login_required
def score_add(request, child_id):
    staff = get_staff_or_403(request)
    child = get_object_or_404(Child, id=child_id)
    if not StaffChildLink.objects.filter(staff=staff, child=child).exists():
        raise PermissionDenied

    if request.method == 'POST':
        form = DevelopmentScoreForm(request.POST)
        if form.is_valid():
            score = form.save(commit=False)
            score.child = child
            score.author = request.user
            score.save()
            messages.success(request, '発達スコアを記録しました。')
            return redirect('daycare:child_growth', child_id=child.id)
    else:
        form = DevelopmentScoreForm(initial={'date': datetime.date.today()})

    return render(request, 'daycare/score_form.html', {
        'form': form, 'child': child,
    })


@login_required
def child_growth(request, child_id):
    """発達グラフページ（支援員・保護者両方が閲覧可）"""
    is_staff = False
    is_parent = False
    try:
        staff = request.user.staff_profile
        if StaffChildLink.objects.filter(staff=staff, child_id=child_id).exists():
            is_staff = True
    except Exception:
        pass

    try:
        parent = request.user.parent_profile
        if ParentChildLink.objects.filter(parent=parent, child_id=child_id).exists():
            is_parent = True
    except Exception:
        pass

    if not (is_staff or is_parent):
        raise PermissionDenied

    child = get_object_or_404(Child, id=child_id)
    scores = list(DevelopmentScore.objects.filter(child=child).order_by('date')[:20])

    chart_data = {
        'labels': [str(s.date) for s in scores],
        'datasets': [
            {'label': '集中力', 'data': [s.focus for s in scores], 'borderColor': '#10b981', 'backgroundColor': 'rgba(16,185,129,0.1)', 'tension': 0.3},
            {'label': 'コミュニケーション', 'data': [s.communication for s in scores], 'borderColor': '#3b82f6', 'backgroundColor': 'rgba(59,130,246,0.1)', 'tension': 0.3},
            {'label': '生活習慣', 'data': [s.daily_living for s in scores], 'borderColor': '#f59e0b', 'backgroundColor': 'rgba(245,158,11,0.1)', 'tension': 0.3},
            {'label': '社会性', 'data': [s.social for s in scores], 'borderColor': '#8b5cf6', 'backgroundColor': 'rgba(139,92,246,0.1)', 'tension': 0.3},
            {'label': '運動・身体', 'data': [s.motor for s in scores], 'borderColor': '#ef4444', 'backgroundColor': 'rgba(239,68,68,0.1)', 'tension': 0.3},
        ]
    }

    latest = scores[-1] if scores else None
    radar_data = None
    if latest:
        radar_data = {
            'labels': ['集中力', 'コミュニケーション', '生活習慣', '社会性', '運動・身体'],
            'data': [latest.focus, latest.communication, latest.daily_living, latest.social, latest.motor]
        }

    return render(request, 'daycare/child_growth.html', {
        'child': child,
        'scores': reversed(scores),
        'chart_data_json': json.dumps(chart_data),
        'radar_data_json': json.dumps(radar_data) if radar_data else 'null',
        'latest': latest,
        'is_staff': is_staff,
        'is_parent': is_parent,
    })
