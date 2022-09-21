from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.dispatch.dispatcher import receiver
from django.shortcuts import redirect, render
from django.urls import conf

from .forms import CustomUserCreationForm, HeartForm, MessageForm, ProfileForm
from .models import Heart, Message, Profile

import numpy as np
import pickle


def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("account")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:

            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET["next"] if "next" in request.GET else "account")

        else:
            messages.error(request, "Username OR password is incorrect")

    return render(request, "users/login_register.html")


def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out!")
    return redirect("login")


def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")

            login(request, user)
            return redirect("edit-account")

        else:
            messages.success(request, "An error has occurred during registration")

    context = {"page": page, "form": form}
    return render(request, "users/login_register.html", context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {"profile": profile, "topSkills": topSkills, "otherSkills": otherSkills}
    return render(request, "users/user-profile.html", context)


@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    heart = Heart.objects.get(owner=profile)
    form = HeartForm(instance=heart)

    context = {"profile": profile, "form": form, "heart": heart}
    return render(request, "users/account.html", context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect("account")

    context = {"form": form}
    return render(request, "users/profile_form.html", context)


@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {"messageRequests": messageRequests, "unreadCount": unreadCount}
    return render(request, "users/inbox.html", context)


@login_required(login_url="login")
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {"message": message}
    return render(request, "users/message.html", context)


def createMessage(request, pk):

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Your message was successfully sent!")
            return redirect("user-profile", pk=recipient.id)

    context = {"recipient": recipient, "form": form}
    return render(request, "users/message_form.html", context)


@login_required(login_url="login")
def ediDetail(request):
    profile = request.user.profile
    heart = Heart.objects.get(owner=profile)

    form = HeartForm(instance=heart)
    if request.method == "POST":
        form = HeartForm(request.POST, instance=heart)

        if form.is_valid():
            heart.owner = profile
            form.save()

        return redirect("account")
    context = {"form": form, "msg": None}
    return render(request, "users/heart_form.html", context)


import pickle
import numpy as np

# Load the Random Forest CLassifier model
# log_model_file = 'logre_model.pkl'
logre = pickle.load(open("./ml_models/logre_model.pkl", "rb"))

# knn_model_file = 'knn_model.pkl'
knn = pickle.load(open("./ml_models/knn_model.pkl", "rb"))

# rf_model_file = 'rf_model.pkl'
rf = pickle.load(open("./ml_models/rf_model.pkl", "rb"))


def checkHeart(request):
    form = HeartForm()
    msg = ""
    if request.method == "POST":
        form = HeartForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data["age"]
            sex = form.cleaned_data["sex"]
            cp = form.cleaned_data["cp"]
            trestbps = form.cleaned_data["trestbps"]
            chol = form.cleaned_data["chol"]
            fbs = form.cleaned_data["fbs"]
            restecg = form.cleaned_data["restecg"]
            thalach = form.cleaned_data["thalach"]
            exang = form.cleaned_data["exang"]
            oldpeak = form.cleaned_data["oldpeak"]
            slope = form.cleaned_data["slope"]
            ca = form.cleaned_data["ca"]
            thal = form.cleaned_data["thal"]

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

        result = ""
        msg = ""
        accuracy = ""
        if "predict1" in request.POST:
            # for knn
            result = knn.predict(data)

        elif "predict2" in request.POST:
            # for logistic regression
            result = logre.predict(data)

        elif "predict3" in request.POST:
            # for random forest
            result = rf.predict(data)

        # result = model.predict(data)

        if result == 1:
            messages.success(request, "You have Chances of Heart Disease!")
        elif result == 0:
            messages.success(request, "Great! You DON'T chances have Heart Disease.")
        print(msg)
    context = {"form": form, "msg": msg}
    return render(request, "users/heart_form.html", context)
