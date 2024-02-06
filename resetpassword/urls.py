from django.urls import path
from . import views

urlpatterns = [
    path('password-reset/', views.PasswordReset.as_view(), name='password-reset'),
    path('password-reset/<encoded_pk>/<token>/', views.ResetPasswordAPI.as_view(), name='reset-password'),
]