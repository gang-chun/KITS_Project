from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import *
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Count, Max, Q
from django.db.models.functions import Greatest

from .filters import StudyFilter

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
def study_list(request):
    studies = Study.objects.all()

    # Filter bar
    myFilter = StudyFilter(request.GET, queryset=studies)
    studies = myFilter.qs

    return render(request, 'KITS/study_list.html', {'studies': studies, 'myFilter': myFilter})


@login_required
def study_detail(request, pk):
    study = get_object_or_404(Study, pk=pk)
    kits = Kit.objects.filter(IRB_number=pk).annotate(
        no_of_kits=Count('kitinstance', filter=Q(kitinstance__status='a'))) \
        .annotate(no_of_kits_exp=Count('kitinstance', filter=Q(kitinstance__status='e'))) \
        .annotate(exp=Max('kitinstance__expiration_date'))
    kit_order = KitOrder.objects.filter(id=pk)
    req = Requisition.objects.filter(study=pk)

    return render(request, 'KITS/study_detail.html', {'study': study, 'kits': kits, 'kit_order': kit_order, 'req': req})


@login_required
def create_study(request):
    if request.method == "POST":
        form = StudyForm(request.POST)
        if form.is_valid():
            new_study = form.save(commit=False)
            new_study.created_date = timezone.now()
            new_study.save()
            studies = Study.objects.filter(start_date__lte=timezone.now())
            return render(request, 'KITS/study_list.html',
                          {'studies': studies})
    else:
        form = StudyForm()
    return render(request, 'KITS/create_study.html', {'form': form})


@login_required
def study_edit(request, pk):
    study = get_object_or_404(Study, pk=pk)
    if request.method == "POST":
        # update
        form = StudyForm(request.POST, instance=study)
        if form.is_valid():
            study = form.save(commit=False)
            study.updated_date = timezone.now()
            study.save()
            study = Study.objects.filter(start_date__lte=timezone.now())
            return render(request, 'KITS/study_list.html',
                          {'studies': study})

    else:
        # edit
        form = StudyForm(instance=study)
    return render(request, 'KITS/study_edit.html', {'form': form})


@login_required
def study_archive(request, pk):
    study = get_object_or_404(Study, pk=pk)
    study.status = 'Closed'
    return redirect('KITS:study_list')


@login_required
def kit_checkin(request):
    if request.method == "POST":
        form = KitForm(request.POST)
        if form.is_valid():
            new_kit = form.save(commit=False)
            new_kit.created_date = timezone.now()
            new_kit.save()
            kit = Kit.objects.filter(date_added__lte=timezone.now())
            return render(request, 'KITS/kit_list.html',
                          {'kit': kit})
    else:
        form = KitForm()
    return render(request, 'KITS/kit_checkin.html', {'form': form})


@login_required
def kit_list(request):
    kit = Kit.objects.all()

    # Filter bar
    # myFilter = KitFilter(request.GET, queryset=kit)
    # kit = myFilter.qs

    return render(request, 'KITS/kit_list.html', {'kit': kit})
    # 'myFilter': myFilter})


@login_required
def kit_edit(request, pk):
    kit = get_object_or_404(Kit, pk=pk)
    if request.method == "POST":
        # update
        form = KitForm(request.POST, instance=kit)
        if form.is_valid():
            kit = form.save(commit=False)
            kit.updated_date = timezone.now()
            kit.save()
            #kit = Kit.objects.filter(start_date__lte=timezone.now())
            return render(request, 'KITS/kit_list.html',
                          {'kit': kit})

    else:
        # edit
        form = KitForm(instance=kit)
    return render(request, 'KITS/kit_edit.html', {'form': form})
