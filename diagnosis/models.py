from django.db import models
import json


JOB_TYPE_CHOICES = [
    ('agriculture', '🌱 農業・園芸系'),
    ('manufacturing', '🔧 製造・組み立て系'),
    ('cleaning', '🧹 清掃・環境整備系'),
    ('food_processing', '🍱 食品加工系'),
    ('service', '🛒 接客・販売補助系'),
]


class DiagnosisSession(models.Model):
    """診断セッション（ログインなしでも使用可能）"""
    session_key = models.CharField(max_length=100, unique=True)
    answers = models.TextField(default='{}')

    # 6特性スコア（各0〜15点程度）
    focus_score = models.IntegerField('集中力', default=0)
    communication_score = models.IntegerField('コミュニケーション力', default=0)
    endurance_score = models.IntegerField('体力・持続力', default=0)
    accuracy_score = models.IntegerField('几帳面さ・正確性', default=0)
    emotion_control_score = models.IntegerField('感情コントロール', default=0)
    learning_score = models.IntegerField('学習意欲・変化への適応', default=0)

    # 診断結果
    job_type = models.CharField('向いている仕事タイプ', max_length=30, choices=JOB_TYPE_CHOICES, blank=True)
    result_strengths = models.TextField(default='[]')
    result_challenges = models.TextField(default='[]')
    result_summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_answers(self):
        return json.loads(self.answers)

    def set_answers(self, data):
        self.answers = json.dumps(data, ensure_ascii=False)

    def get_strengths(self):
        return json.loads(self.result_strengths)

    def get_challenges(self):
        return json.loads(self.result_challenges)

    def get_trait_scores(self):
        return {
            'focus': self.focus_score,
            'communication': self.communication_score,
            'endurance': self.endurance_score,
            'accuracy': self.accuracy_score,
            'emotion_control': self.emotion_control_score,
            'learning': self.learning_score,
        }

    def __str__(self):
        return f"Session {self.session_key[:8]} ({self.created_at.strftime('%Y-%m-%d')})"
