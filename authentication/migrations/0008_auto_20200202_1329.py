# Generated by Django 2.2.9 on 2020-02-02 13:29

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20200202_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='booking_slots',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30')], default='09:00', max_length=95, null=True),
        ),
    ]
