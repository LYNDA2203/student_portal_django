from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Student


@receiver(post_save, sender=UserProfile)
def create_student_for_profile(sender, instance, created, **kwargs):
    
    user = instance.user

    if instance.role == 'student':
        student, created_student = Student.objects.get_or_create(user=user,defaults={'full_name': user.get_full_name() or user.username})

        if created_student:
            print(f"🆕 Created Student for user: {user.username}")
        else:
            print(f"♻️ Student already exists for: {user.username}")

    elif instance.role == 'mentor':
        
        deleted, _ = Student.objects.filter(user=user).delete()
        if deleted:
            print(f"🗑️ Deleted Student record for mentor: {user.username}")


@receiver(post_save, sender=User)
def update_student_profile(sender, instance, **kwargs):

    try:
        user_profile = instance.userprofile
    except UserProfile.DoesNotExist:
        return  

    if user_profile.role == 'student':
        Student.objects.update_or_create(user=instance, defaults={ 'full_name': instance.get_full_name() or instance.username} )
        
        print(f"✅ Synced Student info for user: {instance.username}")
