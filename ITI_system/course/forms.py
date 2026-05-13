from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ("title", "description", "duration_weeks", "cover_image")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "duration_weeks": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "cover_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
