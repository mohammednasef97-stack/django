from django import forms

from .models import Trainee


class TraineeForm(forms.ModelForm):
    class Meta:
        model = Trainee
        fields = ("name", "email", "age", "photo")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 120}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
