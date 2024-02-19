from rest_framework import generics
from .models import Basket
from .serializers import BasketSerializer

class BasketListCreateView(generics.ListCreateAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer

class BasketRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer