from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import *
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

now = timezone.now()


def index(request):
    return render(request, 'registration/login.html')


def login(request):
    return render(request, 'registration/login.html',
                  {'kits': login})


def logout(request):
    return render(request, 'registration/logout.html',
                  {'kits': logout})

def home(request):
    return render(request, 'KITS/home.html')


@login_required
def study(request):
    study = Study.objects.all()
    return render(request, 'KITS/studies.html', {'studies': study})

@login_required
def create_study(request):
   if request.method == "POST":
       form = StudyForm(request.POST)
       if form.is_valid():
           create_study = form.save(commit=False)
           create_study.created_date = timezone.now()
           create_study.save()
           create_study = Study.objects.filter(start_date__lte=timezone.now())
           return render(request, 'KITS/create_study.html',
                         {'create_study': create_study})
   else:
       form = StudyForm()

   return render(request, 'KITS/create_study.html', {'form': form})