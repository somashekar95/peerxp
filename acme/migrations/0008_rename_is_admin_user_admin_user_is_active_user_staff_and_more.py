# Generated by Django 4.1.3 on 2023-02-10 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acme', '0007_alter_user_is_admin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_admin',
            new_name='admin',
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.CharField(max_length=20),
        ),
    ]
