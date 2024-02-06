from django.urls import path, include
from rest_framework import routers
from .views import (
                    favoriteListAPIView,
                    favoriteViewSet,
                    
                    )

router = routers.DefaultRouter()

router.register(r'favorites', favoriteViewSet)



urlpatterns = [
    
    path('favorites/list/',favoriteListAPIView.as_view(), name='favorite-list'),

    path('', include(router.urls)),

]