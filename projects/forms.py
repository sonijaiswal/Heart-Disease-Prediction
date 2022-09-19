from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Project, Review, Heart


class HeartForm(ModelForm):

    class Meta:
        model = Heart
        fields = ['age', 'sex', 'cp', 'trestbps', 'chol',
                  'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

# age = int(request.form['age'])
# sex = request.form.get('sex')
# cp = request.form.get('cp')
# trestbps = int(request.form['trestbps'])
# chol = int(request.form['chol'])
# fbs = request.form.get('fbs')
# restecg = int(request.form['restecg'])
# thalach = int(request.form['thalach'])
# exang = request.form.get('exang')
# oldpeak = float(request.form['oldpeak'])
# slope = request.form.get('slope')
# ca = int(request.form['ca'])
# thal = request.form.get('thal')

    def __init__(self, *args, **kwargs):
        super(HeartForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description',
                  'demo_link', 'source_link', ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update(
        #     {'class': 'input'})

        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
