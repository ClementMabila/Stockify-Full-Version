from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from .models import RestockRequest

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