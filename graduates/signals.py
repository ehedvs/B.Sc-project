from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Profile, Student, AcademicHistory
from registrar_admin.models import Faculty, Program



# sending signal for creating profil
@receiver(post_save, sender=Student)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(student=instance)


@receiver(post_save, sender=AcademicHistory)
def level_of_completion(sender, instance, created, **kwargs):
    dept = Student.objects.get(id=instance.student.id).department
    loc = Student.objects.get(id=instance.student.id).level_of_completion
    status = AcademicHistory.objects.filter(
        student=instance.student.id, academic_status="Promoted").count()
    if dept:
        year_required = Program.objects.get(name=dept).year_required
        status = status/(2*year_required)
        
        Student.objects.filter(id=instance.student.id).update(
            level_of_completion=status*100)

    else:
        Student.objects.filter(id=instance.student.id).update(
            level_of_completion=0.0)


@receiver(post_save, sender=Student)
def update_loc(sender, instance, **kwargs):
    status = AcademicHistory.objects.filter(
        student=instance.id, academic_status="Promoted").count()
    # print(status)
    # print("--------------")
    if instance.department:
        year_required = Program.objects.get(
            name=instance.department).year_required
        status = status/(2*year_required)
        print(status)
        Student.objects.filter(id=instance.id).update(
            level_of_completion=status*100)
    else:
        Student.objects.filter(id=instance.id).update(level_of_completion=0.0)


@receiver(post_delete, sender=AcademicHistory)
def delete_update_loc(sender, instance, **kwargs):
    dept = Student.objects.get(id=instance.student.id).department
    status = AcademicHistory.objects.filter(
        student=instance.student.id, academic_status="promoted").count()
    if dept:
        year_required = Program.objects.get(name=dept).year_required
        status = status/(2*year_required)
        Student.objects.filter(id=instance.student.id).update(
            level_of_completion=status*100)
    else:
        Student.objects.filter(id=instance.id).update(level_of_completion=0.0)
