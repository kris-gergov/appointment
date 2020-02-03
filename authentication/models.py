from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import IntegerField, Model
from multiselectfield import MultiSelectField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('adviser', "Adviser"),
        ('student', "Student"),
    )
    user_type = models.CharField(max_length=20, default='student', choices=TYPE_CHOICES)
    school = models.CharField(max_length=110, blank=True, null=True)
    study_year = IntegerField(
        default=1,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4)
        ]
    )
    SLOT_CHOICES = (
        ('09:00', "09:00"),
        ('09:30', "09:30"),
        ('10:00', "10:00"),
        ('10:30', "10:30"),
        ('11:00', "11:00"),
        ('11:30', "11:30"),
        ('12:00', "12:00"),
        ('12:30', "12:30"),
        ('13:00', "13:00"),
        ('13:30', "13:30"),
        ('14:00', "14:00"),
        ('14:30', "14:30"),
        ('15:00', "15:00"),
        ('15:30', "15:30"),
        ('16:00', "16:00"),
        ('16:30', "16:30"),
    )
    booking_slots = MultiSelectField(choices=SLOT_CHOICES, default='09:00', blank=True, null=True)

    def __str__(self):
        return self.user.username
