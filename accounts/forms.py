from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserSignupForm(UserCreationForm):
    nickname = forms.CharField(
        label='ニックネーム',
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'たとえば：たろう　ゆいちゃん',
            'class': 'w-full border-2 border-green-300 rounded-xl px-4 py-3 text-lg focus:outline-none focus:border-green-500',
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

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            UserProfile.objects.create(
                user=user,
                nickname=self.cleaned_data['nickname'],
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
