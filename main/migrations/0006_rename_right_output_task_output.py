# Generated by Django 3.2.5 on 2022-06-05 21:09

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0005_auto_20220530_0646'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='right_output',
            new_name='output',
        ),
    ]