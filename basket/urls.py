from django.urls import path
from .views import BasketListCreateView, BasketRetrieveUpdateDestroyView
app_name = "basket"
urlpatterns = [
    path('baskets/', BasketListCreateView.as_view(), name='basket-list-create'),
    path('baskets/<int:pk>/', BasketRetrieveUpdateDestroyView.as_view(), name='basket-retrieve-update-destroy'),
]