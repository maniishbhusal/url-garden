# Generated by Django 4.2 on 2023-07-23 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RapidLink', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlmodel',
            name='short_url',
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
    ]
