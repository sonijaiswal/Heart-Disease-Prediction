# Generated by Django 4.1.1 on 2022-09-21 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("name", models.CharField(blank=True, max_length=200, null=True)),
                ("email", models.EmailField(blank=True, max_length=500, null=True)),
                ("username", models.CharField(blank=True, max_length=200, null=True)),
                ("location", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "profile_image",
                    models.ImageField(
                        blank=True,
                        default="profiles/user-default.png",
                        null=True,
                        upload_to="profiles/",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["created"],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("name", models.CharField(blank=True, max_length=200, null=True)),
                ("email", models.EmailField(blank=True, max_length=200, null=True)),
                ("subject", models.CharField(blank=True, max_length=200, null=True)),
                ("body", models.TextField()),
                ("is_read", models.BooleanField(default=False, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "recipient",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="messages",
                        to="users.profile",
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="users.profile",
                    ),
                ),
            ],
            options={
                "ordering": ["is_read", "-created"],
            },
        ),
        migrations.CreateModel(
            name="Heart",
            fields=[
                ("age", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "sex",
                    models.IntegerField(
                        choices=[(0, "Female"), (1, "Male")], default=0
                    ),
                ),
                (
                    "cp",
                    models.IntegerField(
                        choices=[
                            (0, "Typical Angina"),
                            (1, "Atypical Angina"),
                            (2, "Non-Anginal Pain"),
                            (3, "Asymptomatic"),
                        ],
                        default=1,
                    ),
                ),
                ("trestbps", models.IntegerField(blank=True, default=0, null=True)),
                ("chol", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "fbs",
                    models.IntegerField(
                        choices=[
                            (0, "Fasting Blood Sugar < 120 mg/dl"),
                            (1, "Fasting Blood Sugar > 120 mg/dl"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "restecg",
                    models.IntegerField(
                        choices=[
                            (0, "Normal"),
                            (1, "Having ST-T wave abnormality"),
                            (
                                2,
                                "Showing probable or definite left ventricular hypertrophy",
                            ),
                        ],
                        default=0,
                    ),
                ),
                ("thalach", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "exang",
                    models.IntegerField(choices=[(0, "No"), (1, "Yes")], default=0),
                ),
                ("oldpeak", models.FloatField(default=0)),
                (
                    "slope",
                    models.IntegerField(
                        choices=[(0, "Upsloping"), (1, "Flat"), (2, "Downsloping")],
                        default=0,
                    ),
                ),
                ("ca", models.IntegerField(blank=True, default=0, null=True)),
                (
                    "thal",
                    models.IntegerField(
                        choices=[
                            (1, "Normal"),
                            (2, "Fixed Defect"),
                            (3, "Reversible Defect"),
                        ],
                        default=0,
                    ),
                ),
                ("result1", models.IntegerField(blank=True, default=0, null=True)),
                ("result2", models.IntegerField(blank=True, default=0, null=True)),
                ("result3", models.IntegerField(blank=True, default=0, null=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "owner",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.profile",
                    ),
                ),
            ],
        ),
    ]
