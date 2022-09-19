# Generated by Django 4.1.1 on 2022-09-19 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0019_alter_heart_oldpeak"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="heart",
            name="owner",
        ),
        migrations.AlterField(
            model_name="heart",
            name="oldpeak",
            field=models.FloatField(default=0),
        ),
    ]