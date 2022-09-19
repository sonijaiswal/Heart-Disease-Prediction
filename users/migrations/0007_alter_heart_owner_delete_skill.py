# Generated by Django 4.1.1 on 2022-09-19 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_heart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="heart",
            name="owner",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.profile",
            ),
        ),
        migrations.DeleteModel(
            name="Skill",
        ),
    ]