# Generated by Django 5.2 on 2025-04-30 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0014_downloadhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedfile',
            name='seed_count',
            field=models.IntegerField(default=1),
        ),
    ]
