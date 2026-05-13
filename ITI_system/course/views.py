from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from trainee.access import can_manage_courses

from .forms import CourseForm
from .models import Course


def _course_queryset(user):
    return Course.objects.filter(is_deleted=False).order_by("title")


@login_required
def course_list(request):
    courses = _course_queryset(request.user)
    return render(
        request,
        "course/list.html",
        {"courses": courses, "can_manage_courses": can_manage_courses(request.user)},
    )


@login_required
def course_detail(request, id):
    course = get_object_or_404(Course, id=id, is_deleted=False)
    return render(request, "course/detail.html", {"course": course})


@login_required
def add_course(request):
    if not can_manage_courses(request.user):
        messages.error(request, "Only staff or instructors can add courses.")
        return redirect("course:course_list")
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Course created.")
            return redirect("course:course_list")
    else:
        form = CourseForm()
    return render(
        request,
        "course/add.html",
        {
            "form": form,
            "is_edit": False,
            "page_title": "New course",
            "page_subtitle": "Add a title, description, duration, and optional cover image.",
        },
    )


@login_required
def update_course(request, id):
    if not can_manage_courses(request.user):
        messages.error(request, "You cannot edit courses.")
        return redirect("course:course_list")
    course = get_object_or_404(Course, id=id, is_deleted=False)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated.")
            return redirect("course:course_list")
    else:
        form = CourseForm(instance=course)
    return render(
        request,
        "course/update.html",
        {
            "form": form,
            "is_edit": True,
            "course": course,
            "page_title": "Edit course",
            "page_subtitle": course.title,
        },
    )


@login_required
def delete_course(request, id):
    if not can_manage_courses(request.user):
        messages.error(request, "You cannot delete courses.")
        return redirect("course:course_list")
    course = get_object_or_404(Course, id=id, is_deleted=False)
    if request.method == "POST":
        delete_mode = request.POST.get("delete_mode", "soft")
        if delete_mode == "hard":
            course.delete()
            messages.success(request, "Course hard deleted permanently.")
        else:
            course.soft_delete()
            messages.success(request, "Course soft deleted (can be restored from DB).")
        return redirect("course:course_list")
    messages.warning(request, "Deletion must be submitted from the list page.")
    return redirect("course:course_list")
