from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Student

# sending signal for creating profile
@receiver(post_save, sender=Student)
def create_profile(sender, instance, created, **kwargs): 
    if created:
        Profile.objects.create(student=instance)

# @receiver(post_save, sender=Student)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()