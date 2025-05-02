from celery import shared_task
from .models import Stock, Notification
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F

@shared_task
def check_low_stock_and_notify():
    low_stock_products = Stock.objects.filter(quantity__lte=F('product__reorder_level'))
    
    for stock in low_stock_products:
        notification = Notification.objects.create(
            user=stock.product.supplier.user, 
            title="Low Stock Alert", 
            message=f"Stock for {stock.product.name} is running low.",
            notification_type="Stock"
        )
        send_mail(
            "Low Stock Alert",
            f"Stock for {stock.product.name} is running low.",
            settings.DEFAULT_FROM_EMAIL,
            [stock.product.supplier.user.email]
        )

    return "Low stock check complete"
