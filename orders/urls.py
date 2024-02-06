from django.urls import path, include
from rest_framework import routers
from .views import (
                   OrderListAPIView,
                   OrderViewSet,
                    )

router = routers.DefaultRouter()

router.register(r'orders', OrderViewSet)



urlpatterns = [
    path('orders/list/',OrderListAPIView.as_view(), name='order-list'),

    path('', include(router.urls)),

]