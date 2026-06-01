import json
from django.shortcuts import render, redirect
from django.views import View
from .models import RoadmapCache, CAREER_CHOICES
from .services import get_age_groups, get_roadmap_categories, generate_roadmap_with_ai
from diagnosis.services import get_career_list


class CareerSelectView(View):
    def get(self, request):
        career_list = get_career_list()
        suggested_careers = request.session.get('diagnosis_careers', [])
        context = {
            'career_list': career_list,
            'suggested_careers': suggested_careers,
        }
        return render(request, 'roadmap/career_select.html', context)


class RoadmapView(View):
    def get(self, request, career_key):
        age_groups = get_age_groups()
        categories = get_roadmap_categories()
        career_list = get_career_list()

        career_info = next((c for c in career_list if c['key'] == career_key), None)
        if not career_info:
            return redirect('roadmap:career_select')

        selected_age_key = request.GET.get('age', 'lower_elementary')
        selected_age = next((a for a in age_groups if a['key'] == selected_age_key), age_groups[1])

        cached = RoadmapCache.objects.filter(career=career_key, age_group=selected_age_key).first()

        if cached:
            roadmap_data = cached.get_content()
        else:
            roadmap_data = generate_roadmap_with_ai(
                career_key=career_key,
                career_name=career_info['name'],
                age_group_key=selected_age_key,
                age_group_label=f"{selected_age['label']}（{selected_age['range']}）",
            )
            RoadmapCache.objects.create(
                career=career_key,
                career_name=career_info['name'],
                age_group=selected_age_key,
                content=json.dumps(roadmap_data, ensure_ascii=False),
            )

        items = roadmap_data.get('items', {})
        enriched_categories = []
        for cat in categories:
            enriched_categories.append({
                **cat,
                'actions': items.get(cat['key'], []),
            })

        context = {
            'career': career_info,
            'age_groups': age_groups,
            'selected_age': selected_age,
            'categories': enriched_categories,
            'message': roadmap_data.get('message', ''),
            'milestone': roadmap_data.get('milestone', ''),
        }
        return render(request, 'roadmap/roadmap.html', context)
