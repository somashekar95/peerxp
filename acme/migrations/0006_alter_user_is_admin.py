# Generated by Django 4.1.3 on 2023-02-09 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acme', '0005_user_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='admin'),
        ),
    ]
