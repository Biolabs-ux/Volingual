# Generated by Django 5.0.7 on 2024-07-22 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_onetimepassword'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='auth_provider',
            field=models.CharField(default='email', max_length=50, verbose_name='auth provider'),
        ),
    ]
