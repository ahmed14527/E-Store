from rest_framework import generics
from .models import Address
from .serializers import AddressSerializer

class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AddressRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer