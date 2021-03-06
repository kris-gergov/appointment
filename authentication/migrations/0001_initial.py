# Generated by Django 2.2.9 on 2020-01-26 22:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.TextField(max_length=500)),
                ('user_type', models.CharField(choices=[('staff', 'Staff'), ('student', 'Student')], default='student', max_length=20)),
                ('study_year', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(1)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
