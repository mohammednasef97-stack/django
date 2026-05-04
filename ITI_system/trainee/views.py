from django.shortcuts import render, redirect, get_object_or_404
from .models import Trainee
from django.contrib.auth.forms import UserCreationForm
 


def trainee_list(request):
    trainees = Trainee.objects.all()
    return render(request, 'trainee/list.html', {'trainees': trainees})

def add_trainee(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        age = request.POST['age']
        Trainee.objects.create(name=name, email=email, age=age)
        return redirect('trainee:trainee_list')
    return render(request, 'trainee/add.html')

def update_trainee(request, id):
    trainee = get_object_or_404(Trainee, id=id)
    if request.method == 'POST':
        trainee.name = request.POST['name']
        trainee.email = request.POST['email']
        trainee.age = request.POST['age']
        trainee.save()
        return redirect('trainee:trainee_list')
    return render(request, 'trainee/update.html', {'trainee': trainee})

def delete_trainee(request, id):
    trainee = get_object_or_404(Trainee, id=id)
    trainee.delete()
    return redirect('trainee:trainee_list')
def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'trainee/register.html', {'form': form})