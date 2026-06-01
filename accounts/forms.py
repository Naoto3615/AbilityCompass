from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ChildProfile, AGE_GROUP_CHOICES

AVATAR_CHOICES = [
    ('🌟', '🌟 スター'),
    ('🦁', '🦁 ライオン'),
    ('🐬', '🐬 イルカ'),
    ('🦋', '🦋 チョウ'),
    ('🐉', '🐉 ドラゴン'),
    ('🌈', '🌈 虹'),
    ('🚀', '🚀 ロケット'),
    ('⚡', '⚡ 雷'),
    ('🎮', '🎮 ゲーム'),
    ('🎨', '🎨 アート'),
    ('🎵', '🎵 音楽'),
    ('🔭', '🔭 望遠鏡'),
]

CAREER_CHOICES_FORM = [
    ('', '──────── 選んでください ────────'),
    ('programmer', 'プログラマー・エンジニア 💻'),
    ('designer', 'デザイナー・アーティスト 🎨'),
    ('musician', '音楽家・作曲家 🎼'),
    ('scientist', '科学者・研究者 🔬'),
    ('writer', '作家・ライター ✍️'),
    ('mathematician', '数学者・データサイエンティスト 📐'),
    ('game_creator', 'ゲームクリエイター 🎮'),
    ('chef', 'シェフ・料理研究家 👨‍🍳'),
    ('animal_care', '動物の専門家 🐾'),
    ('architect', '建築家・空間デザイナー 🏛️'),
    ('teacher', '教師・支援員 📚'),
    ('athlete', 'スポーツ選手・コーチ ⚽'),
    ('photographer', '写真家・映像作家 📷'),
    ('entrepreneur', '起業家・経営者 🚀'),
    ('doctor', '医師・医療専門家 🩺'),
    ('undecided', 'まだ決まっていない 🌱'),
]

CAREER_NAME_MAP = {
    'programmer': 'プログラマー・エンジニア',
    'designer': 'デザイナー・アーティスト',
    'musician': '音楽家・作曲家',
    'scientist': '科学者・研究者',
    'writer': '作家・ライター',
    'mathematician': '数学者・データサイエンティスト',
    'game_creator': 'ゲームクリエイター',
    'chef': 'シェフ・料理研究家',
    'animal_care': '動物の専門家',
    'architect': '建築家・空間デザイナー',
    'teacher': '教師・支援員',
    'athlete': 'スポーツ選手・コーチ',
    'photographer': '写真家・映像作家',
    'entrepreneur': '起業家・経営者',
    'doctor': '医師・医療専門家',
    'undecided': 'まだ決まっていない',
}


class ChildSignupForm(UserCreationForm):
    nickname = forms.CharField(
        label='ニックネーム',
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'たとえば：たろう、ゆいちゃん'}),
    )
    age_group = forms.ChoiceField(
        label='いまの年齢',
        choices=AGE_GROUP_CHOICES,
    )
    career_goal = forms.ChoiceField(
        label='なりたい職業（あれば）',
        choices=CAREER_CHOICES_FORM,
        required=False,
    )
    avatar_emoji = forms.ChoiceField(
        label='アバターを選ぶ',
        choices=AVATAR_CHOICES,
        widget=forms.RadioSelect,
        initial='🌟',
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': 'ログインID（ローマ字・数字）',
        }

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            career_key = self.cleaned_data.get('career_goal', '')
            ChildProfile.objects.create(
                user=user,
                nickname=self.cleaned_data['nickname'],
                age_group=self.cleaned_data['age_group'],
                career_goal=career_key,
                career_goal_name=CAREER_NAME_MAP.get(career_key, ''),
                avatar_emoji=self.cleaned_data['avatar_emoji'],
            )
        return user


class ParentSignupForm(UserCreationForm):
    child_username = forms.CharField(
        label='お子様のログインID',
        help_text='お子様がすでに登録している場合は入力してください（省略可）',
        required=False,
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {'username': 'ログインID（保護者）'}
