import uuid
from django.shortcuts import render, redirect
from django.views import View
from .models import DiagnosisSession
from .services import get_questions, get_career_list, analyze_with_ai, SCORE_LABELS


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

        questions = get_questions()
        context = {
            'questions': questions,
            'score_labels': SCORE_LABELS,
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
            questions_with_answers = [(q, answers.get(q['id'], 0)) for q in questions]
            unanswered = [q for q, a in questions_with_answers if a == 0]
            context = {
                'questions': questions,
                'score_labels': SCORE_LABELS,
                'answers': answers,
                'total': len(questions),
                'error': f'{len(unanswered)}問まだ答えていません。すべての質問に答えてください。',
            }
            return render(request, 'diagnosis/questions.html', context)

        session, _ = DiagnosisSession.objects.get_or_create(session_key=session_key)
        session.set_answers(answers)

        result = analyze_with_ai(answers)

        import json
        session.result_strengths = json.dumps(result.get('strengths', []), ensure_ascii=False)
        session.result_careers = json.dumps(result.get('careers', []), ensure_ascii=False)
        session.result_summary = result.get('summary', '')
        session.save()

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

        context = {
            'strengths': session.get_strengths(),
            'careers': session.get_careers(),
            'summary': session.result_summary,
            'career_list': get_career_list(),
        }
        return render(request, 'diagnosis/result.html', context)
