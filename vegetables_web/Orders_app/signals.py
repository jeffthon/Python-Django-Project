from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def stock_handle_on_payment(sender, instance, **kwargs):

    if instance.is_paid and not instance.stock_updated:
        for item in instance.items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()
        

        Order.objects.filter(id=instance.id).update(stock_updated=True)