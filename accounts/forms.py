from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, SupporterProfile


class UserSignupForm(UserCreationForm):
    nickname = forms.CharField(
        label='ニックネーム',
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'たとえば：たろう　ゆいちゃん',
            'class': 'w-full border-2 border-green-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-green-500',
        }),
    )
    user_type = forms.ChoiceField(
        label='あなたは？',
        choices=[('adult', '就労を目指す大人'), ('child', '児童（子ども）')],
        widget=forms.RadioSelect(attrs={'class': 'user-type-radio'}),
        initial='adult',
    )
    grade = forms.ChoiceField(
        label='学年',
        choices=[
            ('', '---'),
            ('elementary_low', '小学生（低学年：1〜3年）'),
            ('elementary_high', '小学生（高学年：4〜6年）'),
            ('junior_high', '中学生'),
            ('high_school', '高校生'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full border-2 border-green-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-green-500',
            'id': 'id_grade',
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {
            'username': 'ログインID（ローマ字・数字）',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'hanako123',
                'class': 'w-full border-2 border-green-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-green-500',
            }),
        }

    def __init__(self, *args, text_mode='hiragana', **kwargs):
        super().__init__(*args, **kwargs)
        for fname in ['password1', 'password2']:
            self.fields[fname].widget.attrs.update({
                'class': 'w-full border-2 border-green-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-green-500',
            })

        if text_mode == 'kanji':
            self.fields['nickname'].widget.attrs['placeholder'] = 'たとえば：太郎、ゆいちゃん'
            self.fields['nickname'].error_messages.update({
                'required': 'ニックネームを入力してください',
                'max_length': '30文字以内で入力してください',
            })
            self.fields['username'].error_messages.update({
                'required': 'ログインIDを入力してください',
            })
            self.fields['password1'].error_messages.update({
                'required': 'パスワードを入力してください',
            })
            self.fields['password2'].error_messages.update({
                'required': 'パスワード（確認）を入力してください',
            })
        else:
            self.fields['nickname'].widget.attrs['placeholder'] = 'たとえば：たろう　ゆいちゃん'
            self.fields['nickname'].error_messages.update({
                'required': 'にっくねーむを いれてください',
                'max_length': '30もじ いないで いれてください',
            })
            self.fields['username'].error_messages.update({
                'required': 'ろぐいんIDを いれてください',
            })
            self.fields['password1'].error_messages.update({
                'required': 'ぱすわーどを いれてください',
            })
            self.fields['password2'].error_messages.update({
                'required': 'ぱすわーど（かくにん）を いれてください',
            })

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        grade = cleaned_data.get('grade')
        if user_type == 'child' and not grade:
            self.add_error('grade', '学年を選択してください')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            UserProfile.objects.create(
                user=user,
                nickname=self.cleaned_data['nickname'],
                user_type=self.cleaned_data.get('user_type', 'adult'),
                grade=self.cleaned_data.get('grade', ''),
            )
        return user


class SupporterSignupForm(UserCreationForm):
    target_username = forms.CharField(
        label='支援する人のログインID',
        help_text='すでに登録している場合は入力してください（省略可）',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'ろぐいんID（しょうりゃくか）',
            'class': 'w-full border-2 border-orange-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-orange-500',
        }),
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        labels = {'username': 'ログインID（支援者）'}
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'supporter_taro',
                'class': 'w-full border-2 border-orange-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-orange-500',
            }),
        }

    def __init__(self, *args, text_mode='hiragana', **kwargs):
        super().__init__(*args, **kwargs)
        for fname in ['password1', 'password2']:
            self.fields[fname].widget.attrs.update({
                'class': 'w-full border-2 border-orange-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-orange-500',
            })

        if text_mode == 'kanji':
            self.fields['target_username'].widget.attrs['placeholder'] = 'ログインID（省略可）'
            self.fields['username'].error_messages.update({
                'required': 'ログインIDを入力してください',
            })
            self.fields['password1'].error_messages.update({
                'required': 'パスワードを入力してください',
            })
            self.fields['password2'].error_messages.update({
                'required': 'パスワード（確認）を入力してください',
            })
        else:
            self.fields['target_username'].widget.attrs['placeholder'] = 'ろぐいんID（しょうりゃくか）'
            self.fields['username'].error_messages.update({
                'required': 'ろぐいんIDを いれてください',
            })
            self.fields['password1'].error_messages.update({
                'required': 'ぱすわーどを いれてください',
            })
            self.fields['password2'].error_messages.update({
                'required': 'ぱすわーど（かくにん）を いれてください',
            })

    def clean_target_username(self):
        username = self.cleaned_data.get('target_username', '').strip()
        if not username:
            return username
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('そのログインIDの利用者は見つかりません。IDを確認してください。')
        if not hasattr(target_user, 'user_profile'):
            raise forms.ValidationError('そのIDは利用者アカウントではありません。')
        return username


class AddSupportedUserForm(forms.Form):
    target_username = forms.CharField(
        label='追加する利用者のログインID',
        widget=forms.TextInput(attrs={
            'placeholder': 'ろぐいんID',
            'class': 'w-full border-2 border-orange-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-orange-500',
        }),
    )

    def clean_target_username(self):
        username = self.cleaned_data.get('target_username', '').strip()
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError('そのログインIDの利用者は見つかりません。IDを確認してください。')
        if not hasattr(target_user, 'user_profile'):
            raise forms.ValidationError('そのIDは利用者アカウントではありません。')
        return username
