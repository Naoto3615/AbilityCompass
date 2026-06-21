import uuid
import json
from django.shortcuts import render, redirect
from django.views import View
from .models import DiagnosisSession
from .services import (
    get_questions, get_job_types, analyze_with_ai,
    SCORE_LABELS, SCORE_EMOJIS, TRAIT_LABELS, _calc_trait_scores, _determine_job_type
)
from roadmap.services import resolve_data


JOB_OUTFIT_MAP = {
    'agriculture':    'farming',
    'manufacturing':  'manufacturing',
    'cleaning':       'cleaning',
    'food_processing': 'food',
    'service':        'retail',
}


def _apply_diagnosis_to_avatar(profile, job_type: str, trait_scores: dict) -> None:
    """診断結果をもとにアバター設定を更新する（ユーザーが選んだ外見パーツは保持）。"""
    config = profile.get_avatar_config()

    # 仕事アウトフィット
    config['job_outfit'] = JOB_OUTFIT_MAP.get(job_type, 'none')

    # 特性スコアによるアクセサリー・表情
    comm  = trait_scores.get('communication', 0)
    focus = trait_scores.get('focus', 0)
    endu  = trait_scores.get('endurance', 0)

    # 優先度: 体力 > コミュ > 集中
    if endu >= 3.5:
        config['expression'] = 'happy'
        config['rosy_cheeks'] = True
        config['accessory'] = config.get('accessory', 'none')  # ユーザー選択を尊重
    elif comm >= 3.5:
        config['expression'] = 'happy'
        config['rosy_cheeks'] = False
    else:
        config['expression'] = config.get('expression', 'normal')
        config['rosy_cheeks'] = False

    if focus >= 3.5 and config.get('accessory', 'none') == 'none':
        config['accessory'] = 'glasses'

    profile.avatar_config = config
    profile.save()


class DiagnosisStartView(View):
    def get(self, request):
        return render(request, 'diagnosis/start.html')

    def post(self, request):
        request.session['diagnosis_session_key'] = str(uuid.uuid4())
        return redirect('diagnosis:questions')


class DiagnosisQuestionsView(View):
    def get(self, request):
        session_key = request.session.get('diagnosis_session_key')
        if not session_key:
            return redirect('diagnosis:start')

        text_mode = request.session.get('text_mode', 'hiragana')
        questions = resolve_data(get_questions(), text_mode)
        score_options = [
            {'value': v, 'label': resolve_data(SCORE_LABELS[v], text_mode), 'emoji': SCORE_EMOJIS[v]}
            for v in [1, 2, 3, 4, 5]
        ]
        context = {
            'questions': questions,
            'score_options': score_options,
            'total': len(questions),
        }
        return render(request, 'diagnosis/questions.html', context)

    def post(self, request):
        session_key = request.session.get('diagnosis_session_key')
        if not session_key:
            return redirect('diagnosis:start')

        answers = {}
        for key, value in request.POST.items():
            if key.startswith('q'):
                try:
                    answers[key] = int(value)
                except ValueError:
                    answers[key] = 3

        questions = get_questions()
        if len(answers) < len(questions):
            text_mode = request.session.get('text_mode', 'hiragana')
            score_options = [
                {'value': v, 'label': resolve_data(SCORE_LABELS[v], text_mode), 'emoji': SCORE_EMOJIS[v]}
                for v in [1, 2, 3, 4, 5]
            ]
            unanswered = [q for q in questions if q['id'] not in answers]
            context = {
                'questions': resolve_data(questions, text_mode),
                'score_options': score_options,
                'answers': json.dumps(answers),
                'total': len(questions),
                'error': f'{len(unanswered)}もん　まだこたえていません。すべての　しつもんに　こたえてください。',
            }
            return render(request, 'diagnosis/questions.html', context)

        session, _ = DiagnosisSession.objects.get_or_create(session_key=session_key)
        session.set_answers(answers)

        result = analyze_with_ai(answers)

        trait_scores = result.get('trait_scores', _calc_trait_scores(answers))
        session.focus_score = int(trait_scores.get('focus', 0) * 10)
        session.communication_score = int(trait_scores.get('communication', 0) * 10)
        session.endurance_score = int(trait_scores.get('endurance', 0) * 10)
        session.accuracy_score = int(trait_scores.get('accuracy', 0) * 10)
        session.emotion_control_score = int(trait_scores.get('emotion_control', 0) * 10)
        session.learning_score = int(trait_scores.get('learning', 0) * 10)

        session.job_type = result.get('job_type', _determine_job_type(trait_scores))
        session.result_strengths = json.dumps(result.get('strengths', []), ensure_ascii=False)
        session.result_challenges = json.dumps(result.get('challenges', []), ensure_ascii=False)

        # summary は dict（バイリンガル）か文字列（AI生成）の両方に対応
        summary = result.get('summary', '')
        if isinstance(summary, dict):
            session.result_summary = json.dumps(summary, ensure_ascii=False)
        else:
            session.result_summary = summary
        session.save()

        request.session['diagnosis_job_type'] = session.job_type

        # ─── アバターに診断結果を反映 ────────────────────────────────────────
        if request.user.is_authenticated and hasattr(request.user, 'user_profile'):
            _apply_diagnosis_to_avatar(request.user.user_profile, session.job_type, trait_scores)

        return redirect('diagnosis:result')


class DiagnosisResultView(View):
    def get(self, request):
        session_key = request.session.get('diagnosis_session_key')
        if not session_key:
            return redirect('diagnosis:start')

        try:
            session = DiagnosisSession.objects.get(session_key=session_key)
        except DiagnosisSession.DoesNotExist:
            return redirect('diagnosis:start')

        text_mode = request.session.get('text_mode', 'hiragana')

        trait_scores_raw = {
            'focus': session.focus_score / 10,
            'communication': session.communication_score / 10,
            'endurance': session.endurance_score / 10,
            'accuracy': session.accuracy_score / 10,
            'emotion_control': session.emotion_control_score / 10,
            'learning': session.learning_score / 10,
        }

        # 強み・課題（title/description が bilingual dict の場合も文字列の場合も resolve_data で対応）
        strengths = resolve_data(session.get_strengths(), text_mode)
        challenges = resolve_data(session.get_challenges(), text_mode)

        # 仕事タイプ情報
        raw_job_types = get_job_types()
        raw_job_type_info = next((j for j in raw_job_types if j['key'] == session.job_type), None)
        job_type_info = resolve_data(raw_job_type_info, text_mode) if raw_job_type_info else None

        # summary: JSON文字列（bilingual dict）か plain string かを判定して解決
        raw_summary = session.result_summary
        try:
            parsed_summary = json.loads(raw_summary)
            summary = resolve_data(parsed_summary, text_mode)
        except (json.JSONDecodeError, TypeError, ValueError):
            summary = raw_summary

        # レーダーチャート用データ
        trait_chart_data = [
            {
                'label': resolve_data(TRAIT_LABELS[k]['name'], text_mode),
                'emoji': TRAIT_LABELS[k]['emoji'],
                'score': v,
                'pct': int(v / 5 * 100),
                'key': k,
            }
            for k, v in trait_scores_raw.items()
        ]

        # アバター設定（ログインユーザーのみ）
        avatar_config = None
        show_avatar_prompt = False
        if request.user.is_authenticated and hasattr(request.user, 'user_profile'):
            profile = request.user.user_profile
            avatar_config = profile.get_avatar_config()
            # 'skin' がアバター設定に明示的にない = ユーザーがまだアバターを作成していない
            show_avatar_prompt = 'skin' not in (profile.avatar_config or {})

        context = {
            'session': session,
            'strengths': strengths,
            'challenges': challenges,
            'summary': summary,
            'job_type_info': job_type_info,
            'trait_chart_data': trait_chart_data,
            'trait_chart_json': json.dumps(trait_chart_data, ensure_ascii=False),
            'text_mode': text_mode,
            'avatar_config': avatar_config,
            'show_avatar_prompt': show_avatar_prompt,
        }
        return render(request, 'diagnosis/result.html', context)
