from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class University(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=255, unique=True)
    phone_no1 = PhoneNumberField()
    phone_no2 = PhoneNumberField(blank=True)
    fax_no = PhoneNumberField()
    website = models.URLField(max_length=200)
    pob = models.PositiveSmallIntegerField()
    city = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    def __str__(self):
        return self.name

    




