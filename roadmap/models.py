from django.db import models
import json


AGE_GROUP_CHOICES = [
    ('early_childhood', '幼少期（3〜6歳）'),
    ('lower_elementary', '小学校低学年（7〜9歳）'),
    ('upper_elementary', '小学校高学年（10〜12歳）'),
    ('middle_school', '中学生（13〜15歳）'),
    ('high_school', '高校生（16〜18歳）'),
    ('adult', '大学・社会人（19歳〜）'),
]

CAREER_CHOICES = [
    ('programmer', 'プログラマー・エンジニア'),
    ('designer', 'デザイナー・アーティスト'),
    ('musician', '音楽家・作曲家'),
    ('scientist', '科学者・研究者'),
    ('writer', '作家・ライター'),
    ('mathematician', '数学者・データサイエンティスト'),
    ('game_creator', 'ゲームクリエイター'),
    ('chef', 'シェフ・料理研究家'),
    ('animal_care', '動物の専門家（獣医・トレーナー）'),
    ('architect', '建築家・空間デザイナー'),
    ('teacher', '教師・支援員'),
    ('athlete', 'スポーツ選手・コーチ'),
    ('photographer', '写真家・映像作家'),
    ('entrepreneur', '起業家・経営者'),
    ('doctor', '医師・医療専門家'),
    ('other', 'その他（AI が提案）'),
]


class RoadmapCache(models.Model):
    career = models.CharField(max_length=50, choices=CAREER_CHOICES)
    career_name = models.CharField(max_length=100)
    age_group = models.CharField(max_length=30, choices=AGE_GROUP_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('career', 'age_group')

    def get_content(self):
        return json.loads(self.content)

    def __str__(self):
        return f"{self.career_name} / {self.get_age_group_display()}"
