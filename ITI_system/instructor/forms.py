from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group

from .models import Instructor


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ("name", "age", "salary", "photo")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "min": 18, "max": 100}),
            "salary": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": 0}),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class SignUpForm(UserCreationForm):
    ROLE_INSTRUCTOR = "instructor"
    ROLE_TRAINEE = "trainee"
    ROLE_CHOICES = (
        (ROLE_INSTRUCTOR, "Instructor"),
        (ROLE_TRAINEE, "Trainee"),
    )

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    display_name = forms.CharField(
        label="Full name",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    age = forms.IntegerField(min_value=16, max_value=120, widget=forms.NumberInput(attrs={"class": "form-control"}))
    salary = forms.FloatField(
        required=False,
        min_value=0,
        label="Salary (instructors only)",
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )

    class Meta(UserCreationForm.Meta):
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("username", "password1", "password2"):
            if name in self.fields:
                self.fields[name].widget.attrs.setdefault("class", "form-control")

    def clean(self):
        data = super().clean()
        role = data.get("role")
        if role == self.ROLE_INSTRUCTOR and data.get("salary") in (None, ""):
            self.add_error("salary", "Salary is required for instructor accounts.")
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            role = self.cleaned_data["role"]
            group_name = "Instructor" if role == self.ROLE_INSTRUCTOR else "Trainee"
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
            if role == self.ROLE_INSTRUCTOR:
                Instructor.objects.create(
                    user=user,
                    name=self.cleaned_data["display_name"],
                    age=self.cleaned_data["age"],
                    salary=self.cleaned_data["salary"] or 0,
                )
            else:
                from trainee.models import Trainee

                Trainee.objects.update_or_create(
                    email=self.cleaned_data["email"],
                    defaults={
                        "user": user,
                        "name": self.cleaned_data["display_name"],
                        "age": self.cleaned_data["age"],
                    },
                )
        return user
