from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


CP_CHOICES = (
    (0, 'Typical Angina'),
    (1, 'Atypical Angina'),
    (2, 'Non-Anginal Pain'),
    (3, 'Asymptomatic'),
)

FBS_CHOICES = (
    (0, 'Fasting Blood Sugar < 120 mg/dl'),
    (1, 'Fasting Blood Sugar > 120 mg/dl'),
)

RESTECG_CHOICES = (
    (0, 'Normal'),
    (1, 'Having ST-T wave abnormality'),
    (2, 'Showing probable or definite left ventricular hypertrophy'),

)

EXANG_CHOICES = (
    (0, 'No'),
    (1, 'Yes'),


)

SEX_CHOICES = (
    (0, 'Female'),
    (1, 'Male'),

)

SLOPE_CHOICES = (
    (0, 'Upsloping'),
    (1, 'Flat'),
    (2, 'Downsloping'),
)

THAL_CHOICES = (
    (1, 'Normal'),
    (2, 'Fixed Defect'),
    (3, 'Reversible Defect'),
)



class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    short_intro = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default="profiles/user-default.png")
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['created']

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url


class Heart(models.Model):
    owner = models.OneToOneField(
        Profile, on_delete=models.CASCADE, null=True, blank=True)

    age = models.IntegerField(default=0, null=True, blank=True)
    sex = models.IntegerField(choices=SEX_CHOICES, default=0)
    cp = models.IntegerField(choices=CP_CHOICES, default=1)
    trestbps = models.IntegerField(default=0, null=True, blank=True)
    chol = models.IntegerField(default=0, null=True, blank=True)
    fbs = models.IntegerField(choices=FBS_CHOICES, default=0)
    restecg = models.IntegerField(choices=RESTECG_CHOICES, default=0)
    thalach = models.IntegerField(default=0, null=True, blank=True)
    exang = models.IntegerField(choices=EXANG_CHOICES, default=0)
    oldpeak = models.FloatField(default=0)
    slope = models.IntegerField(choices=SLOPE_CHOICES, default=0)
    ca = models.IntegerField(default=0, null=True, blank=True)
    thal = models.IntegerField(choices=THAL_CHOICES, default=0)

    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

# class Skill(models.Model):
#     owner = models.ForeignKey(
#         Profile, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=200, blank=True, null=True)
#     description = models.TextField(null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True,
#                           primary_key=True, editable=False)

#     def __str__(self):
#         return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
