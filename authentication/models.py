from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import IntegerField, Model


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('staff', "Staff"),
        ('student', "Student"),
    )
    user_type = models.CharField(max_length=20, default='student', choices=TYPE_CHOICES)
    school = models.CharField(max_length=110, blank=True, null=True)
    study_year = IntegerField(
        default=1,
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(4)
        ]
    )

    def __str__(self):
        return self.user.username
