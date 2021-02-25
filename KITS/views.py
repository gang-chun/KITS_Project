from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
# from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect

now = timezone.now()


def index(request):
    return render(request, 'registration/login.html')


def login(request):
    return render(request, 'registration/login.html',
                  {'kits': login})



@login_required
def home(request):
    return render(request, 'KITS/home.html')
