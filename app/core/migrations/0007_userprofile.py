# Generated by Django 4.2.4 on 2023-10-31 23:28

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_recipe_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('picture', models.ImageField(default='NONE', null=True, upload_to=core.models.image_file_path)),
                ('bio', models.CharField(blank=True, max_length=225)),
                ('dob', models.DateField(blank=True, null=True)),
                ('pronouns', models.CharField(choices=[('SHE', 'She/Her'), ('HE', 'He/Him'), ('THEY', 'They/Them'), ('CUSTOM', 'Custom'), ('NONE', 'Prefer not to say')], default='NONE', max_length=20)),
                ('gender', models.CharField(choices=[('FEMALE', 'Female'), ('MALE', 'Male'), ('CUSTOM', 'Custom'), ('NONE', 'Prefer not to say')], default='NONE', max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
