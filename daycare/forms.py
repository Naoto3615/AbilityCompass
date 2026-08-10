from django import forms
from django.contrib.auth.models import User
from .models import Child, DevelopmentScore, SupportRecord


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = ['nickname', 'notes']
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': 'form-input w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
                'placeholder': 'お子さんのニックネーム',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-textarea w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
                'rows': 3,
                'placeholder': '特記事項など（任意）',
            }),
        }


class SupportRecordForm(forms.ModelForm):
    class Meta:
        model = SupportRecord
        fields = ['date', 'content', 'achievement', 'share_with_parent']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
                'rows': 4,
                'placeholder': '今日の支援内容を記録してください',
            }),
            'achievement': forms.Textarea(attrs={
                'class': 'form-textarea w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
                'rows': 3,
                'placeholder': '「できた！」と感じた場面を書いてください（任意）',
            }),
        }


class AddParentForm(forms.Form):
    username = forms.CharField(
        label='保護者のユーザー名',
        widget=forms.TextInput(attrs={
            'class': 'form-input w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': '保護者のユーザー名を入力',
        }),
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.get(username=username)
            if not hasattr(user, 'parent_profile'):
                raise forms.ValidationError('このユーザーは保護者として登録されていません。')
        except User.DoesNotExist:
            raise forms.ValidationError('このユーザー名は存在しません。')
        return username


class DevelopmentScoreForm(forms.ModelForm):
    SCORE_CHOICES = [(i, f'{i}') for i in range(1, 6)]

    focus = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, label='集中力')
    communication = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, label='コミュニケーション')
    daily_living = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, label='生活習慣')
    social = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, label='社会性')
    motor = forms.ChoiceField(choices=SCORE_CHOICES, widget=forms.RadioSelect, label='運動・身体')

    class Meta:
        model = DevelopmentScore
        fields = ['date', 'focus', 'communication', 'daily_living', 'social', 'motor', 'memo']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'memo': forms.Textarea(attrs={'class': 'form-textarea w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400', 'rows': 2, 'placeholder': 'メモ（任意）'}),
        }
