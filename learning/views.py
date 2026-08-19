import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import (
    MannerQuiz, QuizChoice, UserQuizResult,
    DailyScheduleTemplate, ContactNote,
    BookRecord, StampEntry, TalentNote,
    InterviewPractice, INTERVIEW_QUESTIONS, STAMP_TYPES,
)


# ─── クイズ ──────────────────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def quiz_list(request):
    """クイズ一覧（カテゴリ別）"""
    from .models import QUIZ_CATEGORIES
    categories = []
    for key, label in QUIZ_CATEGORIES:
        quizzes = MannerQuiz.objects.filter(category=key)
        answered = UserQuizResult.objects.filter(
            user=request.user, quiz__category=key
        ).values_list('quiz_id', flat=True)
        categories.append({
            'key': key, 'label': label,
            'total': quizzes.count(),
            'answered': len(set(answered)),
        })
    total_correct = UserQuizResult.objects.filter(user=request.user, is_correct=True).count()
    return render(request, 'learning/quiz_list.html', {
        'categories': categories,
        'total_correct': total_correct,
    })


@login_required(login_url='/accounts/login/')
def quiz_play(request, category):
    """クイズを解く（未回答のものをランダムに1問）"""
    import random
    answered_ids = UserQuizResult.objects.filter(
        user=request.user, quiz__category=category
    ).values_list('quiz_id', flat=True)

    unanswered = MannerQuiz.objects.filter(category=category).exclude(id__in=answered_ids)

    if not unanswered.exists():
        all_in_category = MannerQuiz.objects.filter(category=category)
        if not all_in_category.exists():
            # カテゴリに問題がない場合は一覧に戻す
            return redirect('learning:quiz_list')
        # 全問回答済みならリセット（全問再挑戦）
        UserQuizResult.objects.filter(user=request.user, quiz__category=category).delete()
        unanswered = all_in_category

    quiz = random.choice(list(unanswered))
    choices = quiz.choices.all()

    return render(request, 'learning/quiz_play.html', {
        'quiz': quiz,
        'choices': choices,
        'category': category,
    })


@login_required(login_url='/accounts/login/')
def quiz_answer(request, quiz_id):
    """クイズの回答を処理"""
    if request.method != 'POST':
        return redirect('learning:quiz_list')

    quiz = get_object_or_404(MannerQuiz, id=quiz_id)
    choice_id = request.POST.get('choice_id')
    choice = get_object_or_404(QuizChoice, id=choice_id, quiz=quiz)

    result = UserQuizResult.objects.create(
        user=request.user,
        quiz=quiz,
        selected_choice=choice,
        is_correct=choice.is_correct,
    )

    # ポイント付与
    from gamification.models import UserStreak, UserTitle
    streak, _ = UserStreak.objects.get_or_create(user=request.user)
    points = 20 if choice.is_correct else 5
    streak.add_points(points, f'クイズ{"正解" if choice.is_correct else "回答"}')
    streak.total_points += points
    streak.save()
    UserTitle.check_and_award(request.user, streak)

    # スタンプ付与（子どもの場合）
    if hasattr(request.user, 'user_profile') and request.user.user_profile.user_type == 'child':
        StampEntry.objects.create(
            user=request.user, stamp_type='quiz', stamp_emoji='🎓', note='クイズをといた'
        )

    return render(request, 'learning/quiz_result.html', {
        'quiz': quiz,
        'choice': choice,
        'is_correct': choice.is_correct,
    })


# ─── 見通し機能 ───────────────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def schedule_view(request):
    """今日のスケジュール（見通し）"""
    today = timezone.localdate()
    dow = today.weekday()
    template = DailyScheduleTemplate.objects.filter(
        day_of_week=dow, is_active=True
    ).prefetch_related('items').first()

    return render(request, 'learning/schedule.html', {
        'schedule': template,
        'today': today,
    })


# ─── 連絡帳 ──────────────────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def contact_list(request):
    """連絡帳一覧"""
    if hasattr(request.user, 'user_profile') or hasattr(request.user, 'parent_profile'):
        notes = ContactNote.objects.filter(to_user=request.user)
        notes.filter(is_read=False).update(is_read=True)
        is_receiver = True
    else:
        notes = ContactNote.objects.filter(from_user=request.user)
        is_receiver = False

    return render(request, 'learning/contact_list.html', {
        'notes': notes, 'is_receiver': is_receiver
    })


@login_required(login_url='/accounts/login/')
def contact_write(request):
    """連絡帳を書く（支援員用）"""
    from daycare.models import Child, StaffChildLink
    if request.method == 'POST':
        ContactNote.objects.create(
            from_user=request.user,
            to_user_id=request.POST.get('to_user_id'),
            date=request.POST.get('date'),
            mood=int(request.POST.get('mood', 3)),
            content=request.POST.get('content', ''),
            homework=request.POST.get('homework', ''),
        )
        return redirect('learning:contact_list')

    # 支援員の担当児童の保護者を取得
    parents = []
    if hasattr(request.user, 'staff_profile'):
        links = StaffChildLink.objects.filter(staff=request.user.staff_profile).select_related('child')
        for link in links:
            from daycare.models import ParentChildLink
            parent_links = ParentChildLink.objects.filter(child=link.child).select_related('parent__user')
            for pl in parent_links:
                parents.append({'user': pl.parent.user, 'child': link.child})

    return render(request, 'learning/contact_write.html', {
        'parents': parents,
        'today': timezone.localdate(),
    })


# ─── 読書記録 ─────────────────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def book_list(request):
    """読書記録一覧"""
    books = BookRecord.objects.filter(user=request.user)
    if request.method == 'POST':
        BookRecord.objects.create(
            user=request.user,
            title=request.POST.get('title', ''),
            comment=request.POST.get('comment', ''),
            rating=int(request.POST.get('rating', 3)),
            read_at=request.POST.get('read_at', timezone.localdate()),
        )
        # スタンプ付与
        if hasattr(request.user, 'user_profile') and request.user.user_profile.user_type == 'child':
            StampEntry.objects.create(
                user=request.user, stamp_type='read', stamp_emoji='📖', note='ほんをよんだ'
            )
        return redirect('learning:book_list')
    return render(request, 'learning/book_list.html', {'books': books})


# ─── スタンプラリー ────────────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def stamp_rally(request):
    """スタンプラリー（子ども向け）"""
    stamps = StampEntry.objects.filter(user=request.user).order_by('-earned_at')[:30]
    stamp_counts = {}
    for s in stamps:
        stamp_counts[s.stamp_type] = stamp_counts.get(s.stamp_type, 0) + 1

    return render(request, 'learning/stamp_rally.html', {
        'stamps': stamps,
        'stamp_counts': stamp_counts,
        'stamp_types': STAMP_TYPES,
        'total': stamps.count(),
    })


# ─── 得意なことノート ──────────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def talent_notes(request):
    """得意なことノート"""
    notes = TalentNote.objects.filter(user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        emoji = request.POST.get('emoji', '⭐')
        if content:
            TalentNote.objects.create(
                user=request.user,
                content=content,
                emoji=emoji,
                date=timezone.localdate(),
            )
            # スタンプ付与
            if hasattr(request.user, 'user_profile') and request.user.user_profile.user_type == 'child':
                StampEntry.objects.create(
                    user=request.user, stamp_type='record', stamp_emoji='📒', note='きろくした'
                )
        return redirect('learning:talent_notes')
    return render(request, 'learning/talent_notes.html', {'notes': notes})


# ─── クールダウンコーナー ──────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def cooldown(request):
    """クールダウンコーナー（深呼吸・気持ち落ち着かせ）"""
    return render(request, 'learning/cooldown.html')


# ─── 模擬面接練習 ──────────────────────────────────────────────────────────────

@login_required(login_url='/accounts/login/')
def interview_practice(request):
    """模擬面接練習"""
    practices = InterviewPractice.objects.filter(user=request.user)
    practiced_ids = set(practices.values_list('question_id', flat=True))

    if request.method == 'POST':
        qid = request.POST.get('question_id')
        answer = request.POST.get('answer', '').strip()
        if qid and answer:
            # AI フィードバック（APIなしのフォールバック）
            feedback = _generate_interview_feedback(answer)
            InterviewPractice.objects.create(
                user=request.user,
                question_id=qid,
                answer=answer,
                ai_feedback=feedback,
            )
            # ポイント付与
            from gamification.models import UserStreak
            streak, _ = UserStreak.objects.get_or_create(user=request.user)
            streak.add_points(15, '模擬面接練習')
            streak.total_points += 15
            streak.save()
        return redirect('learning:interview_practice')

    return render(request, 'learning/interview_practice.html', {
        'questions': INTERVIEW_QUESTIONS,
        'practices': {p.question_id: p for p in practices},
        'practiced_ids': practiced_ids,
    })


def _generate_interview_feedback(answer: str) -> str:
    """面接回答にフィードバックを生成（OpenAIが使えない場合はルールベース）"""
    try:
        from django.conf import settings
        from openai import OpenAI
        api_key = getattr(settings, 'OPENAI_API_KEY', None)
        if not api_key:
            raise Exception('no key')
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{
                'role': 'system',
                'content': '就労支援の模擬面接コーチです。回答を100字以内で優しく評価してください。'
            }, {
                'role': 'user',
                'content': f'面接の回答：{answer}'
            }],
            max_tokens=150,
        )
        return response.choices[0].message.content
    except Exception:
        length = len(answer)
        if length < 20:
            return '💡 もう少し詳しく話すと良いですよ！具体的なエピソードを加えてみましょう。'
        elif length < 50:
            return '👍 いいですね！もう少し自分の気持ちや理由も伝えるとさらに良くなります。'
        else:
            return '🌟 とても良い回答です！自分の言葉でしっかり伝えられています。練習を続けましょう！'
