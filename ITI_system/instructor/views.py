 
from django.shortcuts import render, redirect
from .models import Instructor
from django.contrib.auth.forms import UserCreationForm


def instructorList(request):

    instructors = Instructor.objects.all()

    context = {
        'instructors': instructors
    }

    return render(
        request,
        'instructor/list.html',
        context
    )


def addInstructor(request):

    if request.method == 'POST':

        name = request.POST['name']
        age = request.POST['age']
        salary = request.POST['salary']

        Instructor.objects.create(
            name=name,
            age=age,
            salary=salary
        )

        return redirect('/instructor/list')

    return render(
        request,
        'instructor/add.html'
    )


def deleteInstructor(request, id):

    instructor = Instructor.objects.get(id=id)

    instructor.delete()

    return redirect('/instructor/list')
 
 

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    return render(request, 'login.html')