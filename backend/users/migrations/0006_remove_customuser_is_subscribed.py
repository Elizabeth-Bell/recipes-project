# Generated by Django 3.2.3 on 2023-10-16 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_subscribe_unique_subscription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_subscribed',
        ),
    ]
