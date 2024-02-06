from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path
from .views import LogoutView

urlpatterns = [
    path('sign-in/', LoginAPI.as_view(), name='sign-in'),
    path('sign-out/', LogoutView.as_view(), name='sign-out'),
    path('signup/', RegisterAPI.as_view(), name='signup'),

]