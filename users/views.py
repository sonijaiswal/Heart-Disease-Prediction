from django.dispatch.dispatcher import receiver
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from django.db.models import Q
from .models import Profile, Message, Heart
from .forms import CustomUserCreationForm, ProfileForm, MessageForm, HeartForm
from .utils import searchProfiles, paginateProfiles

import pickle
import numpy as np

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('account')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(
                request, 'An error has occurred during registration')

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def profiles(request):

    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 3)
    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile': profile, 'topSkills': topSkills,
               "otherSkills": otherSkills}
    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    # skills = profile.skill_set.all()
    # projects = profile.project_set.all()
    

    context = {'profile': profile, 'skills': None, 'projects': None}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your message was successfully sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {'recipient': recipient, 'form': form}
    return render(request, 'users/message_form.html', context)
#################################################################

def editHeart(request):
    page = 'edit-heart'
    profile = request.user.profile
    heart = Heart.objects.get(owner=profile)
    form = HeartForm(instance=heart)
    if request.method == 'POST':
        form = HeartForm(request.POST, instance=heart)
        if form.is_valid():
            form.save()

        return redirect('account')

    context = {'form': form,'page':page}
    return render(request, 'users/heart_form.html', context)


######### ML works ########################
# Load the Random Forest CLassifier model
logre = pickle.load(open('./ml_models/logre_model.pkl', 'rb'))
knn = pickle.load(open('./ml_models/knn_model.pkl', 'rb'))
rf = pickle.load(open('./ml_models/rf_model.pkl', 'rb'))

@login_required(login_url="login")
def checkHeart(request):
    profile = request.user.profile
    heart = Heart.objects.get(owner=profile)

    form = HeartForm(instance=heart)
    msg = ''
    if request.method == "POST":
        form = HeartForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data['age']
            sex = form.cleaned_data['sex']
            cp = form.cleaned_data['cp']
            trestbps = form.cleaned_data['trestbps']
            chol = form.cleaned_data['chol']
            fbs = form.cleaned_data['fbs']
            restecg = form.cleaned_data['restecg']
            thalach = form.cleaned_data['thalach']
            exang = form.cleaned_data['exang']
            oldpeak = form.cleaned_data['oldpeak']
            slope = form.cleaned_data['slope']
            ca = form.cleaned_data['ca']
            thal = form.cleaned_data['thal']

        data = np.array([[age, sex, cp, trestbps, chol, fbs,
                        restecg, thalach, exang, oldpeak, slope, ca, thal]])

        result = ''
        accuracy = ''
        if 'predict1' in request.POST:
            result = knn.predict(data)

        elif 'predict2' in request.POST:
            result = logre.predict(data)

        elif 'predict3' in request.POST:
            result = rf.predict(data)

        # result = model.predict(data)

        if result == 1:
            messages.error(request, 'You have Chances of Heart Disease')
            msg = "You have Chances of Heart Disease"

        elif result == 0:
            messages.success(request, 'Great! You DON \'T chances have Heart Disease.')
            msg = "Great! You DON'T chances have Heart Disease."
        
    context = {
        'form': form,
        'msg': None
    }
    return render(request, "users/heart_form.html", context)


"""
    if request.method == 'POST':
        form = HeartForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = HeartForm()

"""


"""

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')

    context = {'object': skill}
    return render(request, 'delete_template.html', context)
"""
