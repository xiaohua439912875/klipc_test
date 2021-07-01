import json
from django.shortcuts import render
import stripe
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt

YOUR_DOMAIN = 'http://localhost:8000'

import uuid
stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
stripe.client_id = "12313131"

# If you are testing your webhook locally with the Stripe CLI you
# can find the endpoint's secret by running `stripe listen`
# Otherwise, find your endpoint's secret in your webhook settings in the Developer Dashboard
endpoint_secret = 'whsec_ay6CFgDIp6AshUNeypEvn8xvyRqrFNG5'


class StripeOrder(View):
    """
    支付
    """
    def post(self, request):
        """
        接收前端请求参数
        处理请求,将stripe checkout_session id 返回出去，构建支付页面
        :param request:
        :return:
        """

        # 1 接收请求参数 余额
        currency = request.POST.get("currency")  # 货币类型
        amount = request.POST.get("amount")   # 余额
        quantity = request.POST.get("quantity")  # 数量

        # 2 将请求的参数, 发送到 stripe.checkout.Session.create 方法中
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': 2000,
                            'product_data': {
                                'name': 'Stubborn Attachments',
                                'images': ['https://i.imgur.com/EHyR2nP.png'],
                            },
                        },
                        'quantity': 1,

                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/stripe_hooks',
                cancel_url=YOUR_DOMAIN + '/cancel.html',
            )
            print({"id": checkout_session.id})
            # 3 得到stripe 响应之后，返回 checkout session id 返回给前端
            return JsonResponse({"id": checkout_session.id})
        except Exception as e:
            # log
            print(e)
            pass



class StripeCallback(View):

    def get(self, request):

        return render(request, "checkout.html")

    @csrf_exempt
    def post(self, request):
        payload = request.body
        event = None
        # print(payload)
        try:
            event = stripe.Event.construct_from(
                json.loads(payload), stripe.api_key
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)

        # Handle the event
        if event.type == 'payment_intent.succeeded':
            print("333")
            payment_intent = event.data.object  # contains a stripe.PaymentIntent
            # Then define and call a method to handle the successful payment intent.
            # handle_payment_intent_succeeded(payment_intent)
        elif event.type == 'payment_method.attached':
            print("ccc")
            payment_method = event.data.object  # contains a stripe.PaymentMethod

            print(payment_method)
            # Then define and call a method to handle the successful attachment of a PaymentMethod.
            # handle_payment_method_attached(payment_method)
            # ... handle other event types
        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)




