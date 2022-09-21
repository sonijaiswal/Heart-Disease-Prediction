import pickle

import numpy as np
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Heart, Profile

# @receiver(post_save, sender=Profile)

######### ML works ########################
# Load the Random Forest CLassifier model
logre = pickle.load(open("./ml_models/logre_model.pkl", "rb"))
knn = pickle.load(open("./ml_models/knn_model.pkl", "rb"))
rf = pickle.load(open("./ml_models/rf_model.pkl", "rb"))


def ValuePredictor(input_data, algo):
    result = algo.predict(input_data)
    return result


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        subject = "Welcome to the Website"
        message = "We are glad you are here!"

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def createHeart(sender, instance, created, **kwargs):
    if created:
        profile = instance
        heart = Heart.objects.create(owner=profile)


def updateHeart(sender, instance, created, **kwargs):
    heart = Heart.objects.get(owner=instance.owner)

    if created == False:
        age = heart.age
        sex = heart.sex
        cp = heart.cp
        trestbps = heart.trestbps
        chol = heart.chol
        fbs = heart.fbs
        restecg = heart.restecg
        thalach = heart.thalach
        exang = heart.exang
        oldpeak = heart.oldpeak
        slope = heart.slope
        ca = heart.ca
        thal = heart.thal

        data = np.array(
            [
                [
                    age,
                    sex,
                    cp,
                    trestbps,
                    chol,
                    fbs,
                    restecg,
                    thalach,
                    exang,
                    oldpeak,
                    slope,
                    ca,
                    thal,
                ]
            ]
        )

        knn_res = ValuePredictor(data, knn)
        logre_res = ValuePredictor(data, logre)
        rf_res = ValuePredictor(data, rf)
        print("We are glad you are here!")
        Heart.objects.filter(owner=instance.owner).update(
            owner=instance.owner, result1=knn_res, result2=logre_res, result3=rf_res
        )
        # heart.save()


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)

post_save.connect(createHeart, sender=Profile)
post_save.connect(updateHeart, sender=Heart)
