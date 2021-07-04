from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.stripc import views

router = DefaultRouter()

urlpatterns = [
    # 支付请求接口
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view()),
    # 支付回调接口
    path('stripe_webhooks/', views.stripe_webhook),
    # checkout html test url
    path('checkout/', views.CheckoutClike.as_view()),
    path('success/', views.Success.as_view()),
    path('chancel/', views.Cancel.as_view()),

]