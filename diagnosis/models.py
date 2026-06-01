from django.db import models
import json


class DiagnosisSession(models.Model):
    session_key = models.CharField(max_length=100, unique=True)
    answers = models.TextField(default='{}')
    result_strengths = models.TextField(default='[]')
    result_careers = models.TextField(default='[]')
    result_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_answers(self):
        return json.loads(self.answers)

    def set_answers(self, data):
        self.answers = json.dumps(data, ensure_ascii=False)

    def get_strengths(self):
        return json.loads(self.result_strengths)

    def get_careers(self):
        return json.loads(self.result_careers)

    def __str__(self):
        return f"Session {self.session_key[:8]} ({self.created_at.strftime('%Y-%m-%d')})"
