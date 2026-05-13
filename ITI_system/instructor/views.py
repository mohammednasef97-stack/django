from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from trainee.access import can_manage_instructors, is_portal_admin

from .forms import InstructorForm, SignUpForm
from .models import Instructor


@login_required
def instructor_list(request):
    if not can_manage_instructors(request.user):
        messages.error(request, "You do not have access to the instructor directory.")
        return redirect("course:course_list")
    instructors = Instructor.objects.filter(is_deleted=False).order_by("name")
    return render(request, "instructor/list.html", {"instructors": instructors})


@login_required
def instructor_detail(request, id):
    if not can_manage_instructors(request.user):
        messages.error(request, "You do not have access to the instructor directory.")
        return redirect("course:course_list")
    instructor = get_object_or_404(Instructor, id=id, is_deleted=False)
    return render(request, "instructor/detail.html", {"instructor": instructor})


@login_required
def add_instructor(request):
    if not can_manage_instructors(request.user):
        messages.error(request, "You cannot add instructors.")
        return redirect("course:course_list")
    if request.method == "POST":
        form = InstructorForm(request.POST, request.FILES)
        if form.is_valid():
            inst = form.save(commit=False)
            inst.user = None
            inst.save()
            messages.success(request, "Instructor profile saved.")
            return redirect("instructor:instructor_list")
    else:
        form = InstructorForm()
    return render(
        request,
        "instructor/add.html",
        {
            "form": form,
            "is_edit": False,
            "page_title": "Add instructor",
            "page_subtitle": "Create a roster entry with optional profile photo.",
        },
    )


@login_required
def update_instructor(request, id):
    if not can_manage_instructors(request.user):
        messages.error(request, "You cannot edit instructors.")
        return redirect("course:course_list")
    instructor = get_object_or_404(Instructor, id=id, is_deleted=False)
    if request.method == "POST":
        form = InstructorForm(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, "Instructor profile updated.")
            return redirect("instructor:instructor_list")
    else:
        form = InstructorForm(instance=instructor)
    return render(
        request,
        "instructor/add.html",
        {
            "form": form,
            "is_edit": True,
            "instructor": instructor,
            "page_title": "Edit instructor",
            "page_subtitle": instructor.name,
        },
    )


@login_required
def delete_instructor(request, id):
    if not can_manage_instructors(request.user):
        messages.error(request, "You cannot delete instructors.")
        return redirect("course:course_list")
    instructor = get_object_or_404(Instructor, id=id, is_deleted=False)
    if request.method == "POST":
        delete_mode = request.POST.get("delete_mode", "soft")
        if delete_mode == "hard":
            instructor.delete()
            messages.success(request, "Instructor hard deleted permanently.")
        else:
            instructor.soft_delete()
            messages.success(
                request,
                "Instructor soft deleted (can be restored from DB).",
            )
        return redirect("instructor:instructor_list")
    messages.warning(request, "Deletion must be submitted from the list page.")
    return redirect("instructor:instructor_list")


def register(request):
    # Allow anonymous self-registration and admin-created accounts.
    if request.user.is_authenticated and not is_portal_admin(request.user):
        messages.error(request, "Only admin can create additional accounts.")
        return redirect("home")
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if request.user.is_authenticated and is_portal_admin(request.user):
                messages.success(
                    request,
                    f"Account '{user.username}' created successfully.",
                )
                return redirect("home")
            login(request, user)
            messages.success(request, "Account created. You are now signed in.")
            return redirect("home")
    return render(request, "register.html", {"form": form})
