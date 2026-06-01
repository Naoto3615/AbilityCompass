from django.db import models
from django.contrib.auth.models import User


AGE_GROUP_CHOICES = [
    ('early_childhood', '幼少期（3〜6歳）'),
    ('lower_elementary', '小学校低学年（7〜9歳）'),
    ('upper_elementary', '小学校高学年（10〜12歳）'),
    ('middle_school', '中学生（13〜15歳）'),
    ('high_school', '高校生（16〜18歳）'),
    ('adult', '大学・社会人（19歳〜）'),
]

BADGE_DEFINITIONS = {
    'first_task':    {'name': '初めての一歩', 'emoji': '👣', 'desc': '初めてタスクを完了した'},
    'week_streak':   {'name': '7日連続', 'emoji': '🔥', 'desc': '7日連続でタスクを完了した'},
    'emotion_log_5': {'name': '気持ちの記録家', 'emoji': '📔', 'desc': '感情ログを5日間記録した'},
    'points_100':    {'name': '100ポイント達成', 'emoji': '⭐', 'desc': '合計100ポイントを獲得した'},
    'points_500':    {'name': '500ポイント達成', 'emoji': '🏆', 'desc': '合計500ポイントを獲得した'},
    'all_categories':{'name': 'バランスの達人', 'emoji': '🌈', 'desc': 'すべてのカテゴリのタスクを完了した'},
}


class ChildProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='child_profile')
    nickname = models.CharField('ニックネーム', max_length=30)
    career_goal = models.CharField('目標の職業', max_length=50, blank=True)
    career_goal_name = models.CharField('職業名', max_length=100, blank=True)
    age_group = models.CharField('年齢フェーズ', max_length=30, choices=AGE_GROUP_CHOICES, default='lower_elementary')
    total_points = models.IntegerField('合計ポイント', default=0)
    badges = models.TextField('バッジ', default='[]')
    avatar_emoji = models.CharField('アバター絵文字', max_length=10, default='🌟')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_badges(self):
        import json
        return json.loads(self.badges)

    def add_badge(self, badge_key):
        import json
        current = self.get_badges()
        if badge_key not in current:
            current.append(badge_key)
            self.badges = json.dumps(current)
            self.save()
            return True
        return False

    def get_level(self):
        if self.total_points < 50:
            return 1, '探索者', '🔍'
        elif self.total_points < 150:
            return 2, '挑戦者', '⚡'
        elif self.total_points < 350:
            return 3, '成長者', '🌱'
        elif self.total_points < 700:
            return 4, '輝く星', '⭐'
        else:
            return 5, 'レジェンド', '🏆'

    def get_age_group_label(self):
        return dict(AGE_GROUP_CHOICES).get(self.age_group, '')

    def __str__(self):
        return f"{self.nickname} ({self.user.username})"


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    children = models.ManyToManyField(ChildProfile, blank=True, related_name='parents')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"保護者: {self.user.username}"
