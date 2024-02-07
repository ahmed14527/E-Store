from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path
from .views import LogoutView
from . import views

urlpatterns = [
    path('sign-in/', LoginAPI.as_view(), name='sign-in'),
    path('sign-out/', LogoutView.as_view(), name='sign-out'),
    path('signup/', RegisterAPI.as_view(), name='signup'),
    path('userinfo/', views.current_user,name='user_info'),
    #path('forgot_password/', views.forgot_password,name='forgot_password'), 
    #path('reset_password/<str:token>', views.reset_password,name='reset_password'), 
]