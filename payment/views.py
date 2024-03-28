from http.client import NOT_FOUND
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cart
from order.models import PaymentHistory, Order, OrderProduct
from order.serializers import PostOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Payment session created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={"sessionId": openapi.Schema(type=openapi.TYPE_STRING)},
                ),
            ),
        },
    )
    def post(self, request):
        user = self.request.user

        try:
            cart = user.cart
        except Cart.DoesNotExist:
            raise NotFound("Cart not found")
        except user.DoesNotExist:
            raise NotFound("User not found")

        total_price = sum([cart_product.quantity * cart_product.product.price for cart_product in cart.cartproduct_set.all()])

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
              'price_data': {
                'currency': 'usd',
                'unit_amount': int(total_price * 100),
                'product_data': {
                  'name': 'Your purchase',
                },
              },
              'quantity': 1,
            }],
            mode='payment',
            success_url=settings.SITE_URL + '/orders',
            cancel_url=settings.SITE_URL + '/cart',
            metadata={'user_id': request.user.id}
        )

        for cart_product in cart.cartproduct_set.all():
            PaymentHistory.objects.create(
                user=request.user,
                product=cart_product.product,
                payment_status=False
            )

        return JsonResponse({'sessionId': session.url})

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'intent_id': openapi.Schema(type=openapi.TYPE_STRING),
                'status': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def put(self, request):
        intent_id = request.data.get('intent_id')
        status = request.data.get('status')

        intent = stripe.PaymentIntent.retrieve(intent_id)

        if status == 'succeeded':
            user_id = intent.metadata['user_id']
            user = user.objects.get(id=user_id)
            cart = user.cart

stripe.api_key = 'sk_test_51N4C2MCnAe4mWFw2TKo8V3gkpZAfU7YE7oJF0MAJUZakxSOjm6jXC01q2knSLXfNI0moAvwoSF9Vhm9setmKAqJ400kB90PKWO'

@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_SECRET_WEBHOOK
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        customer_email = session['customer_details']['email']

        if event['type'] == 'checkout.session.completed':
            intent = event['data']['object']
            user_id = intent['metadata']['user_id']
            user = user.objects.get(id=user_id)
            cart = user.cart
            cart_products = cart.cartproduct_set.all()
            order_data = {
                'user': user_id,
                'payment_method': 'visa',
            }

            serializer = PostOrderSerializer(data=order_data)
            if serializer.is_valid():
                order = serializer.save()
                for cart_product in cart_products:
                    OrderProduct.objects.create(order=order, product=cart_product.product, quantity=cart_product.quantity)
                    cart_product.product.quantity -= cart_product.quantity
                    cart_product.product.save()
                    PaymentHistory.objects.create(user=user, product=cart_product.product, payment_status=True)
                cart.delete()
                return HttpResponse({'message': 'Order added successfully', 'order': serializer.data}, status=status.HTTP_201_CREATED)
            return HttpResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponse(status=200)