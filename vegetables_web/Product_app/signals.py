from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Product

@receiver(post_save, sender=Product)
def notify_farmer_on_approval(sender, instance, created, **kwargs):
    
    if not created and instance.is_verified:
        farmer_email = instance.farmer.email
        product_name = instance.name
        
        subject = f"Good News! Your product '{product_name}' is Approved"
        message = f"Hello {instance.farmer.username},\n\nYour product '{product_name}' has been verified and approved by the admin. It is now live on the marketplace for customers to buy!"
        from_email = 'noreply@vegetablemarket.com'
        
        try:
            send_mail(subject, message, from_email, [farmer_email])
        except Exception as e:
            print(f"Failed to send email: {e}")