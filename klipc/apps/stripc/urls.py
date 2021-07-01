from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.stripc import views

router = DefaultRouter()


urlpatterns = [
    # 支付请求接口
    path('create-checkout-session/', views.StripeOrder.as_view()),
    # 支付回调接口
    path('stripe_hooks/', views.StripeCallback.as_view()),
    path('checkout/', views.StripeCallback.as_view()),
    # 查询订单结果
    # # 汇合订单
    # path('consolidate_order/', views.Consolidate_Order.as_view())
]