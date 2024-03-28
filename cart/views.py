from cart.serializers import CartSerializer, AddToCartSerializer, UpdateCartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import Product
from cart.models import Cart, CartProduct
from django.shortcuts import get_object_or_404
from rest_framework import status, serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AddToCartSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Product added successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "product": openapi.Schema(type=openapi.TYPE_OBJECT),
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Error in serializer",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT, properties={"error": openapi.Schema(type=openapi.TYPE_OBJECT)}
                ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = AddToCartSerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product added successfully', 'product': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Cart found",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"message": openapi.Schema(type=openapi.TYPE_STRING), "cart": openapi.Schema(type=openapi.TYPE_OBJECT)},
                ),
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response({'message': 'Cart found', 'cart': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'action': openapi.Schema(type=openapi.TYPE_STRING),
                'product': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Product Updated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "message": openapi.Schema(type=openapi.TYPE_STRING),
                        "product": openapi.Schema(type=openapi.TYPE_OBJECT),
                    },
                ),
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Error in serializer",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT, properties={"error": openapi.Schema(type=openapi.TYPE_OBJECT)}
                ),
            ),
        },
    )
    def put(self, request, *args, **kwargs):
        user = request.user
        action = request.data.get('action')
        product = request.data.get('product')
        cart, created = Cart.objects.get_or_create(user=user)

        try:
            cart_product = CartProduct.objects.get(cart=cart, product=product)
        except CartProduct.DoesNotExist:
            raise serializers.ValidationError({'message': 'Product not found'}, code=status.HTTP_404_NOT_FOUND)

        serializer = UpdateCartSerializer(cart_product, data=request.data, context={'action': action, 'product': product})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product Updated successfully', 'product': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='product',
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description='Product ID',
                required=True,
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: openapi.Response(description="Product deleted successfully"),
        },
    )
    def delete(self, request, *args, **kwargs):
        product_id = kwargs['product']
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        product = get_object_or_404(Product, id=product_id)
        cart_product = get_object_or_404(CartProduct, cart=cart, product=product)
        cart_product.delete()
        return Response({'message': 'Productdeleted successfully'}, status=status.HTTP_204_NO_CONTENT)