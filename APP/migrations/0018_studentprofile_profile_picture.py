# Generated by Django 5.1.7 on 2025-04-30 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0017_uploadedfile_seed_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='profile_picture',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
