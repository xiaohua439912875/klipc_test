from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
import uuid
# Create your models here.

class Stripe(models.Model):
    """
    信用卡支付
    """
    CUR_TYPE = (
        (1, 'CNY'),
        (2, 'USD')
    )

    ORDER_STATUS = (
        (0, "待支付"),
        (1, "支付成功"),
        (2, "支付失败"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency_type = models.IntegerField(choices=CUR_TYPE, default=2, verbose_name="货币类型")
    amount = models.DecimalField(decimal_places=2, max_digits=20, verbose_name="充值金额")
    act_currency_type = models.IntegerField(choices=CUR_TYPE, default=2, verbose_name="实际交易货币类型")
    order_status = models.IntegerField(choices=ORDER_STATUS, default=0, verbose_name="订单状态")
    content = models.CharField(max_length=128, verbose_name="内容")
    quantity = models.CharField(max_length=128, verbose_name="数量")
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

