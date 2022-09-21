from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Heart, Message, Profile


class HeartForm(ModelForm):
    class Meta:
        model = Heart
        fields = [
            "age",
            "sex",
            "cp",
            "trestbps",
            "chol",
            "fbs",
            "restecg",
            "thalach",
            "exang",
            "oldpeak",
            "slope",
            "ca",
            "thal",
        ]
        labels = {
            "age": "Age",
            "sex": "Sex",
            "cp": "Chest Pain Type(cp)",
            "trestbps": "Resting Blood Pressure(rbp)",
            "chol": "Serum Cholestoral(chol)",
            "fbs": "Fasting Blood Sugar(fbs)",
            "restecg": "Resting ElectroCardioGraphic(restecg)",
            "thalach": "Maximum Heart Rate Achieved(thalach)",
            "exang": "Exercise Enduced Angina(exang)",
            "oldpeak": "ST depression induced(oldpeak)",
            "slope": "the slope of the peak exercise ST segment(slope)",
            "ca": "number of major vessels(ca)",
            "thal": "Thalessemia(thal)",
        }

    def __init__(self, *args, **kwargs):
        super(HeartForm, self).__init__(*args, **kwargs)
        self.fields["oldpeak"] = forms.FloatField(max_value=6, min_value=1)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {
            "first_name": "Name",
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "name",
            "email",
            "username",
            "location",
            "profile_image",
        ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "subject", "body"]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "input"})
