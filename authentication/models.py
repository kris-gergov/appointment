from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import IntegerField, Model
from django.core.validators import MaxValueValidator, MinValueValidator


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('staff', "Staff"),
        ('student', "Student"),
    )
    user_type = models.CharField(max_length=20, default='student', choices=TYPE_CHOICES)
    study_year = IntegerField(
        default=1,
        validators=[
            MaxValueValidator(4),
            MinValueValidator(1)
        ]
    )

    def __str__(self):
        return self.user.username
