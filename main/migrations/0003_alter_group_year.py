# Generated by Django 3.2.5 on 2022-05-30 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_rename_actionfile_action"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="year",
            field=models.PositiveSmallIntegerField(verbose_name="дата создания"),
        ),
    ]