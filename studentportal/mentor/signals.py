# signals.py
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create UserProfile automatically if it doesn't exist
        UserProfile.objects.create(user=instance)
    else:
        # Save if it exists
        if hasattr(instance, "userprofile"):
            instance.userprofile.save()
