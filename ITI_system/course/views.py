from django.shortcuts import render, redirect, get_object_or_404
from .models import Course

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course/list.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        duration_weeks = request.POST['duration_weeks']
        Course.objects.create(title=title, description=description, duration_weeks=duration_weeks)
        return redirect('course:course_list')
    return render(request, 'course/add.html')

def update_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        course.title = request.POST['title']
        course.description = request.POST['description']
        course.duration_weeks = request.POST['duration_weeks']
        course.save()
        return redirect('course:course_list')
    return render(request, 'course/update.html', {'course': course})

def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect('course:course_list')
