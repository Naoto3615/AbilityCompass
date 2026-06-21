import json
from django.shortcuts import render, redirect
from django.views import View
from .services import get_step_definitions, get_job_roadmap, resolve_data
from diagnosis.services import get_job_types


class JobTypeSelectView(View):
    def get(self, request):
        text_mode = request.session.get('text_mode', 'hiragana')
        job_types = resolve_data(get_job_types(), text_mode)
        suggested_job_type = request.session.get('diagnosis_job_type', '')
        context = {
            'job_types': job_types,
            'suggested_job_type': suggested_job_type,
        }
        return render(request, 'roadmap/job_select.html', context)


class RoadmapView(View):
    def get(self, request, job_type_key):
        text_mode = request.session.get('text_mode', 'hiragana')

        raw_job_types = get_job_types()
        job_info_raw = next((j for j in raw_job_types if j['key'] == job_type_key), None)
        if not job_info_raw:
            return redirect('roadmap:job_select')
        job_info = resolve_data(job_info_raw, text_mode)

        step_defs = resolve_data(get_step_definitions(), text_mode)
        roadmap_data = resolve_data(get_job_roadmap(job_type_key), text_mode)

        steps = []
        for step_num in [1, 2, 3]:
            step_def = step_defs[step_num]
            step_key = f"step{step_num}"
            step_content = roadmap_data.get(step_key, {})
            steps.append({
                **step_def,
                'number': step_num,
                'tasks': step_content.get('tasks', []),
                'message': step_content.get('message', ''),
            })

        context = {
            'job_info': job_info,
            'steps': steps,
            'job_type_key': job_type_key,
            'text_mode': text_mode,
        }
        return render(request, 'roadmap/roadmap.html', context)
