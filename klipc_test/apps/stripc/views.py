import json
from django.shortcuts import render
import stripe
from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.views import View
from django.views.decorators.csrf import csrf_exempt

YOUR_DOMAIN = 'http://121.4.107.137:8000/'

import uuid
# stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'
stripe.api_key = 'sk_test_Z0MbREXbYPkF4NOBEjUJheD7'

stripe.client_id = "12313131"

# If you are testing your webhook locally with the Stripe CLI you
# can find the endpoint's secret by running `stripe listen`
# Otherwise, find your endpoint's secretdestination in your webhook settings in the Developer Dashboard
# endpoint = stripe.WebhookEndpoint.create(
#   url='http://121.4.107.137:8000/stripe_webhooks/',
#   enabled_events=[
#     'charge.failed',
#     'charge.succeeded',
#   ],
# )
endpoint_secret = 'whsec_7luLZjmsydHdZ8cwBVBQaeHRLLNgGGCz'

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



class CreateCheckoutSessionView(View):
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
            metadata={
                "user_id": "11131313"
            },
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })




@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        print(session)

    elif event["type"] == "payment_intent.succeeded":
        intent = event['data']['object']

        print(intent)


    return HttpResponse(status=200)







