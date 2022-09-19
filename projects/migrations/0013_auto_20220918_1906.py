# Generated by Django 3.2.4 on 2022-09-18 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20220918_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='exang',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='thalach',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]