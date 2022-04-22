from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import AdminLoginForm


# topページ
class HomeView(TemplateView):
  template_name = 'home.html'


# ログイン
class AdminLoginView(LoginView):
  template_name = 'admin_login.html'
  authentication_form = AdminLoginForm

  def form_valid(self, form):
    remember = form.cleaned_data['remember']
    if remember:
      self.request.session.set_expiry(1200000)
    return super().form_valid(form)


# ログアウト
class AdminLogoutView(LogoutView):
  pass
