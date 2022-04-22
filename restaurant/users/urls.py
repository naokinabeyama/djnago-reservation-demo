from django.urls import path
from .views import AdminLogoutView, HomeView, AdminLoginView 

app_name = 'users'

urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('admin_login', AdminLoginView.as_view(), name='admin_login'),
    path('admin_logout', AdminLogoutView.as_view(), name='admin_logout')
]
