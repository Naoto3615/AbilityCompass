from django.db import models
from django.contrib.auth.models import User


class Child(models.Model):
    nickname = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='child_profile',
        verbose_name='利用者アカウント',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}（支援員）"


class StaffChildLink(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='children')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='staff_links')

    class Meta:
        unique_together = ('staff', 'child')

    def __str__(self):
        return f"{self.staff} → {self.child}"


class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}（保護者）"


class ParentChildLink(models.Model):
    parent = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name='children')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='parent_links')

    class Meta:
        unique_together = ('parent', 'child')


class SupportRecord(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='records')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.TextField(verbose_name='支援記録')
    achievement = models.TextField(blank=True, verbose_name='今日のできた！')
    share_with_parent = models.BooleanField(default=False, verbose_name='保護者に共有する')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.child.nickname} - {self.date}"


class DevelopmentScore(models.Model):
    INDICATORS = [
        ('focus', '集中力'),
        ('communication', 'コミュニケーション'),
        ('daily_living', '生活習慣'),
        ('social', '社会性'),
        ('motor', '運動・身体'),
    ]

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='development_scores')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    focus = models.IntegerField(default=3, choices=[(i, i) for i in range(1, 6)])
    communication = models.IntegerField(default=3, choices=[(i, i) for i in range(1, 6)])
    daily_living = models.IntegerField(default=3, choices=[(i, i) for i in range(1, 6)])
    social = models.IntegerField(default=3, choices=[(i, i) for i in range(1, 6)])
    motor = models.IntegerField(default=3, choices=[(i, i) for i in range(1, 6)])
    memo = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.child.nickname} - {self.date}"

    def to_dict(self):
        return {
            'date': str(self.date),
            'focus': self.focus,
            'communication': self.communication,
            'daily_living': self.daily_living,
            'social': self.social,
            'motor': self.motor,
        }
