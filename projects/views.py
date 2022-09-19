from django.forms.models import model_to_dict
from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm, HeartForm
from .utils import searchProjects, paginateProjects
import pickle
import numpy as np

# Load the Random Forest CLassifier model
# log_model_file = 'logre_model.pkl'
logre = pickle.load(open('logre_model.pkl', 'rb'))

# knn_model_file = 'knn_model.pkl'
knn = pickle.load(open('knn_model.pkl', 'rb'))

# rf_model_file = 'rf_model.pkl'
rf = pickle.load(open('rf_model.pkl', 'rb'))


@login_required(login_url="login")
def checkHeart(request):
    profile = request.user.profile
    form = HeartForm()
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
        msg = ''
        accuracy = ''
        if 'predict1' in request.POST:
            # for knn
            result = knn.predict(data)

        elif 'predict2' in request.POST:
            # for logistic regression
            result = logre.predict(data)

        elif 'predict3' in request.POST:
            # for random forest
            result = rf.predict(data)

        # result = model.predict(data)

        if result == 1:
            msg = "You have Chances of Heart Disease"

        elif result == 0:
            msg = "Great! You DON'T chances have Heart Disease."
        print(msg)
    context = {
        'form': form,
        'msg': msg
    }
    return render(request, "projects/heart_form.html", context)


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


def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Your review was successfully submitted!')
        return redirect('project', pk=projectObj.id)

    return render(request, 'projects/single-project.html', {'project': projectObj, 'form': form})


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',',  " ").split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context = {'form': form, 'project': project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)
