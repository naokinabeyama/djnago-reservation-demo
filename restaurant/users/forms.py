from django.contrib.auth.forms import AuthenticationForm
from django import forms


# ログインフォーム
class AdminLoginForm(AuthenticationForm):
  # このusernameは一意を識別するもの(emailをunique=Trueにしている)
  username = forms.EmailField(label='メールアドレス')
  password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
  remember = forms.BooleanField(label='ログイン状態を保持する', required=False)
