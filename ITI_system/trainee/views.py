from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView

from .access import can_manage_trainees, is_instructor, is_portal_admin, is_trainee_group
from .forms import TraineeForm
from .models import Trainee


class StaffOrInstructorMixin(UserPassesTestMixin):
    def test_func(self):
        return can_manage_trainees(self.request.user)


def trainee_queryset_for(user):
    if not user.is_authenticated:
        return Trainee.objects.none()
    if is_portal_admin(user) or is_instructor(user):
        return Trainee.objects.filter(is_deleted=False)
    if is_trainee_group(user):
        return Trainee.objects.filter(user=user, is_deleted=False)
    return Trainee.objects.none()


def _can_edit_trainee(user, trainee):
    if can_manage_trainees(user):
        return True
    return is_trainee_group(user) and trainee.user_id == user.id


def _can_view_trainee(user, trainee):
    if can_manage_trainees(user):
        return True
    return is_trainee_group(user) and trainee.user_id == user.id


@login_required
def trainee_list(request):
    trainees = trainee_queryset_for(request.user).order_by("-join_date", "name")
    return render(
        request,
        "trainee/list.html",
        {"trainees": trainees, "can_manage_trainees": can_manage_trainees(request.user)},
    )


@login_required
def trainee_detail(request, id):
    trainee = get_object_or_404(Trainee, id=id, is_deleted=False)
    if not _can_view_trainee(request.user, trainee):
        messages.error(request, "You cannot view this trainee record.")
        return redirect("trainee:trainee_list")
    return render(request, "trainee/detail.html", {"trainee": trainee})


@login_required
def add_trainee_fbv(request):
    """Function-based insert: explicit GET/POST with ModelForm validation."""
    if not can_manage_trainees(request.user):
        messages.error(request, "You do not have permission to add trainees.")
        return redirect("trainee:trainee_list")

    if request.method == "POST":
        form = TraineeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Trainee saved using a function-based view and ModelForm.",
            )
            return redirect("trainee:trainee_list")
    else:
        form = TraineeForm()
    return render(
        request,
        "trainee/add.html",
        {
            "form": form,
            "is_edit": False,
            "pattern_label": "Function-based insert",
            "pattern_detail": "GET shows an empty ModelForm; POST runs is_valid(), then form.save().",
            "page_title": "New trainee",
            "page_subtitle": "Function-based view + ModelForm",
        },
    )


class TraineeGenericCreateView(LoginRequiredMixin, StaffOrInstructorMixin, CreateView):
    """Generic editing view: CreateView + ModelForm (Django’s built-in insert workflow)."""

    model = Trainee
    form_class = TraineeForm
    template_name = "trainee/add.html"
    success_url = reverse_lazy("trainee:trainee_list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Trainee saved using generic CreateView and the same ModelForm.",
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["is_edit"] = False
        ctx["pattern_label"] = "Generic CreateView + ModelForm"
        ctx["pattern_detail"] = (
            "CreateView wires the ModelForm, handles invalid POST, and redirects on success."
        )
        ctx["page_title"] = "New trainee"
        ctx["page_subtitle"] = "Generic CreateView + ModelForm"
        return ctx


class TraineeManualInsertCBV(LoginRequiredMixin, StaffOrInstructorMixin, View):
    """Custom CBV insert: View subclass with manual GET/POST (still uses ModelForm)."""

    template_name = "trainee/add.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "form": TraineeForm(),
                "is_edit": False,
                "pattern_label": "Custom CBV insert",
                "pattern_detail": "View.get/post with TraineeForm — no CreateView base class.",
                "page_title": "New trainee",
                "page_subtitle": "Custom class-based View + ModelForm",
            },
        )

    def post(self, request):
        form = TraineeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Trainee saved using a custom class-based view and ModelForm.",
            )
            return redirect("trainee:trainee_list")
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "is_edit": False,
                "pattern_label": "Custom CBV insert",
                "pattern_detail": "Validation failed; errors are attached to the form.",
                "page_title": "New trainee",
                "page_subtitle": "Custom class-based View + ModelForm",
            },
        )


@login_required
def update_trainee(request, id):
    trainee = get_object_or_404(Trainee, id=id, is_deleted=False)
    if not _can_edit_trainee(request.user, trainee):
        messages.error(request, "You cannot edit this trainee record.")
        return redirect("trainee:trainee_list")

    if request.method == "POST":
        form = TraineeForm(request.POST, request.FILES, instance=trainee)
        if form.is_valid():
            form.save()
            messages.success(request, "Trainee profile updated.")
            return redirect("trainee:trainee_list")
    else:
        form = TraineeForm(instance=trainee)
    return render(
        request,
        "trainee/update.html",
        {
            "form": form,
            "pattern_label": "Update trainee",
            "pattern_detail": "Same ModelForm in edit mode (instance=trainee).",
            "is_edit": True,
            "page_title": "Edit trainee",
            "page_subtitle": trainee.name,
        },
    )


@login_required
def delete_trainee(request, id):
    if not can_manage_trainees(request.user):
        messages.error(request, "Only staff or instructors may delete trainees.")
        return redirect("trainee:trainee_list")
    trainee = get_object_or_404(Trainee, id=id, is_deleted=False)
    if request.method == "POST":
        delete_mode = request.POST.get("delete_mode", "soft")
        if delete_mode == "hard":
            trainee.delete()
            messages.success(request, "Trainee hard deleted permanently.")
        else:
            trainee.soft_delete()
            messages.success(request, "Trainee soft deleted (can be restored from DB).")
        return redirect("trainee:trainee_list")
    messages.warning(request, "Deletion must be submitted from the list page.")
    return redirect("trainee:trainee_list")
