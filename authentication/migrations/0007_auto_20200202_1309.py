# Generated by Django 2.2.9 on 2020-02-02 13:09

import django.core.validators
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20200129_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='booking_slots',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30')], default='09:00', max_length=95),
        ),
        migrations.AlterField(
            model_name='profile',
            name='study_year',
            field=models.IntegerField(blank=True, default=1, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.CharField(choices=[('adviser', 'Adviser'), ('student', 'Student')], default='student', max_length=20),
        ),
    ]
