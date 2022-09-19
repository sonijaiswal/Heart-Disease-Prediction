# Generated by Django 3.2.4 on 2022-09-18 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_project_test1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='test1',
            field=models.IntegerField(choices=[(1, 'Typical Angina'), (2, 'Atypical Angina'), (3, 'Non-Anginal Pain'), (4, 'Asymptomatic')], default=1),
        ),
    ]