from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from .models import RestockRequest, StockHistory, Stock

@receiver(post_save, sender=User)
def create_user_group(sender, instance, created, **kwargs):
    if created:
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            print("Admin group created")
        else:
            print("Admin group already exists")

        # Similarly for other groups
        Group.objects.get_or_create(name='Investor')
        Group.objects.get_or_create(name='Supplier')
        Group.objects.get_or_create(name='Financial Admin')

@receiver(pre_save, sender=RestockRequest)
def mark_restock_as_seen(sender, instance, **kwargs):
    if not instance.seen:
        instance.seen = True
        
@receiver(post_save, sender='API.Stock')
def update_stock_from_restock(sender, instance, created, **kwargs):
    """Update stock levels when a restock occurs"""
    # Skip if this save was from within increase_stock or reduce_stock methods
    if hasattr(instance, '_skip_signal') and instance._skip_signal:
        return
        
    if created or instance.tracker.has_changed('quantity'):
        stock = instance.product.stock
        
        # Avoid recursion - only update if this isn't the same instance
        if stock.pk != instance.pk:
            old_quantity = stock.quantity
            
            # Use our controlled method to update the quantity
            # This will set _skip_signal internally
            stock.increase_stock(instance.quantity)
            
            StockHistory.objects.create(
                organization=instance.organization,
                transaction_type='Restock',
                product=instance.product,
                sku=instance.product.sku,
                stock_change=instance.quantity,
                starting_stock=old_quantity,
                notes=f"Restock #{instance.id}"
            )