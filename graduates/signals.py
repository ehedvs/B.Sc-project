from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Student, AcademicHistory
from registrar_admin.models import Faculty, Program

# sending signal for creating profile
@receiver(post_save, sender=Student)
def create_profile(sender, instance, created, **kwargs): 
    if created:
        Profile.objects.create(student=instance)

# @receiver(post_save, sender=Student)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()

@receiver(post_save, sender=AcademicHistory)
def level_of_completion(sender, instance, created, **kwargs):
    dept = Student.objects.get(id=instance.student.id).department
    loc = Student.objects.get(id=instance.student.id).level_of_completion
    if dept:
        year_required = Program.objects.get(name=dept).year_required
        print(instance.academic_status)
        if instance.academic_status == "promoted":
            if (instance.semester % 2)==0:
                loc = (instance.semester*instance.batch)*(1/(year_required*2))
                loc = loc*100
            else:
                loc = (2*instance.batch-instance.semester)*(1/(year_required*2))
                loc = loc*100

            Student.objects.filter(id=instance.student.id).update(level_of_completion=loc)

        else:
            pass
        
    else:
        print("yelam")




