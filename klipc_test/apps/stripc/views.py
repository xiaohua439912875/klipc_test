import json
from django.shortcuts import render
import stripe
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt

YOUR_DOMAIN = '121.4.107.137'

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
        amount = request.POST.get("amount")   # 余额 × 100
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
                        'description': "My First Test Charge (created for API docs)",
                        'quantity': 1,

                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
            print({"id": checkout_session.id})
            # 3 得到stripe 响应之后，返回 checkout session id 返回给前端
            return JsonResponse({"id": checkout_session.id})

        except Exception as e:
            # log
            print(e)
            pass


class StripeCallback(View):

    @csrf_exempt
    def post(self, request):
        payload = request.body
        event = None
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']

        # print(payload)

        try:
            # 检查 验证Stripe 是否从官方发送过来的
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        try:
            # 当验证成功会收到 charge.succeeded事件处理
            event = stripe.Event.construct_from(
                json.loads(payload), stripe.api_key, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)

        # Handle the event
        # type事件类型
        if event.type == 'payment_intent.succeeded':
            # 支付费用成功，处理业务逻辑
            # 1 接收来自 stripe 的响应数据,对进行出来
            # 主要处理字段 metadata status amount id
            payment_intent = event.data.object  # contains a stripe.PaymentIntent
            # Then define and call a method to handle the successful payment intent.
            # handle_payment_intent_succeeded(payment_intent)
            amount = payment_intent["amount"]# 支付余额
            amount_received = payment_intent["amount_received"]  # 实际接收金额
            # description = payment_intent.description  # 描述信息
            # charges 额外信息,例如用户填入的邮箱、地址、姓名 账单明细等 取 charges["metadata"]
            metadata = payment_intent["charges"]["data"][0]["metadata"]
            print(amount)
            print(amount_received)
            print(metadata)

            # 2 用户逻辑处理

        elif event.type == 'payment_method.attached':
            # Occurs whenever a new payment method is attached to a customer.
            payment_method = event.data.object  # contains a stripe.PaymentMethod
            # Then define and call a method to handle the successful attachment of a PaymentMethod.
            # handle_payment_method_attached(payment_method)

        else:
            print('Unhandled event type {}'.format(event.type))

        return HttpResponse(status=200)


class CheckoutClike(View):
    """模拟前端点击页面"""

    def get(self, request):

        return render(request, "checkout.html")

class Success(View):

    def get(self, request):

        return render(request, "success.html")

class Cancel(View):

    def get(self, reqeust):

        return render(reqeust, "cancel.html")
