from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Student, Mentor
from django.db.models import Q

@receiver(post_save, sender=UserProfile)
def sync_user_related_models(sender, instance, created, **kwargs):
    user = instance.user
    full_name = user.get_full_name() or user.username

    # If role = STUDENT
    if instance.role == 'student':
        # Find any existing student by user or same full_name (case-insensitive)
        student_qs = Student.objects.filter(Q(user=user) | Q(full_name__iexact=full_name))
        student = student_qs.first()

        if student:
            # ✅ Update missing fields only
            if not student.full_name:
                student.full_name = full_name
            if not student.user_id:
                student.user = user
            student.save()

            # 🧹 Remove duplicates if any
            student_qs.exclude(id=student.id).delete()
            print(f"✅ Synced existing student: {student.full_name}")
        else:
            # ✅ Create if not found
            Student.objects.create(user=user, full_name=full_name)
            print(f"🆕 Created new student: {full_name}")

        # 🔥 Ensure no mentor record exists for this user
        Mentor.objects.filter(user=user).delete()

    # 🧩 If role = MENTOR
    elif instance.role == 'mentor':
        mentor_qs = Mentor.objects.filter(Q(user=user) | Q(full_name__iexact=full_name))
        mentor = mentor_qs.first()

        if mentor:
            if not mentor.full_name:
                mentor.full_name = full_name
            if not mentor.user_id:
                mentor.user = user
            mentor.save()
            mentor_qs.exclude(id=mentor.id).delete()
            print(f"✅ Synced existing mentor: {mentor.full_name}")
        else:
            Mentor.objects.create(user=user, full_name=full_name)
            print(f"🆕 Created new mentor: {full_name}")

        # 🔥 Remove old student record if exists
        Student.objects.filter(user=user).delete()
        
@receiver(post_save, sender=User)
def update_student_name_on_user_change(sender, instance, **kwargs):
   
    try:
        profile = instance.userprofile
        if profile.role == 'student':
            Student.objects.filter(user=instance).update(full_name=instance.get_full_name() or instance.username)
            
    except UserProfile.DoesNotExist:
        pass
