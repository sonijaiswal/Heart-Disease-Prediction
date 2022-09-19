from django.db import models
import uuid

from django.db.models.deletion import CASCADE
from users.models import Profile

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
    (0, 'Normal'),
    (1, 'Fixed Defect'),
    (2, 'Reversible Defect'),
)


class Heart(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField(default=0, null=True, blank=True)
    sex = models.IntegerField(choices=SEX_CHOICES, default=0)
    cp = models.IntegerField(choices=CP_CHOICES, default=1)
    trestbps = models.IntegerField(default=0, null=True, blank=True)
    chol = models.IntegerField(default=0, null=True, blank=True)
    fbs = models.IntegerField(choices=FBS_CHOICES, default=0)
    restecg = models.IntegerField(choices=RESTECG_CHOICES, default=0)
    thalach = models.IntegerField(default=0, null=True, blank=True)
    exang = models.IntegerField(choices=EXANG_CHOICES, default=0)
    oldpeak = models.FloatField(default=0, null=True, blank=True)
    slope = models.IntegerField(choices=SLOPE_CHOICES, default=0)
    ca = models.IntegerField(default=0, null=True, blank=True)

    thal = models.IntegerField(choices=THAL_CHOICES, default=0)

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    # def __str__(self):
    #     return self.id


class Project(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField("Tag", blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-vote_ratio", "-vote_total", "title"]

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ""
        return url

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list("owner__id", flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value="up").count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio

        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ("up", "Up Vote"),
        ("down", "Down Vote"),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        unique_together = [["owner", "project"]]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name
