from django.urls import path
from .views import AddressListCreateView, AddressRetrieveUpdateDestroyView

urlpatterns = [
    path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressRetrieveUpdateDestroyView.as_view(), name='address-retrieve-update-destroy'),
]