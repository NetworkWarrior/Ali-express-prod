from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Welcome to Global-Bazaar',
            f'hello {instance.username}, welcome to Global-Bazaar, find your favourite product among millions of best choices',
            'akmalllakmal5@gmail.com',
            [instance.email]
        )
