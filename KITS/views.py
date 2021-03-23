from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import *
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Count, Max, Q
from django.db.models.functions import Greatest

from .filters import StudyFilter, KitFilter

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


def home2(request):
    return render(request, 'KITS/home2.html')


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
        no_of_kits=Count('kit', filter=Q(kit__status='a'))) \
        .annotate(no_of_kits_exp=Count('kit', filter=Q(kit__status='e'))) \
        .annotate(exp=Max('kit__expiration_date'))
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
    study.save()
    return redirect('KITS:study_list')


@login_required
def kit_addkittype(request):

    if request.method == "POST":
        form = KitForm(request.POST)
        if form.is_valid():
            new_kit = form.save(commit=False)
            new_kit.created_date = timezone.now()
            new_kit.save()
            Kit.objects.filter(date_added__lte=timezone.now())
            return redirect('KITS:kit_list')
    else:
        form = KitForm()
    return render(request, 'KITS/kit_addkittype.html', {'form': form})


@login_required
def kit_list(request):
    kit = Kit.objects.all()
    # Filter bar
    myFilter = KitFilter(request.GET, queryset=kit)
    kit = myFilter.qs
    return render(request, 'KITS/kit_list.html', {'kit': kit, 'myFilter': myFilter})

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
            # kit = Kit.objects.filter(start_date__lte=timezone.now())
            return redirect('KITS:kit_list')
    else:
        # edit
        form = KitForm(instance=kit)
    return render(request, 'KITS/kit_edit.html', {'form': form,})


@login_required
def kit_delete(request, pk):
   kit = get_object_or_404(Kit, pk=pk)
   kit.delete()
   return redirect('KITS:kit_list')

#kits = Kit.objects.filter(id=pk)
@login_required
def kit_addkitinstance(request, pk):
    kit_instance = get_object_or_404(Kit, pk=pk)
    #kit_instance = Kit.objects.filter(id=pk)

    if request.method == "POST":
        form = KitInstanceForm(request.POST)
        if form.is_valid():



            #new_kitinstance = KitInstance.objects.get(form.cleaned_data['pk'])
            new_kitinstance = form.save(commit=False)
            new_kitinstance.kit_id = pk
            #new_kitinstance.created_date = timezone.now()
            new_kitinstance.kit_id = pk
            new_kitinstance.save()
            #KitInstance.objects.filter(date_added__lte=timezone.now())

            return redirect('KITS:kit_list')
    else:
        form = KitInstanceForm()
    return render(request, 'KITS/kit_addkitinstance.html', {'form': form, 'kit_instance': kit_instance})


@login_required
def kitinstance_add(request, pk):

    new_kitinstance = get_object_or_404(KitInstance, pk=pk)
    if request.method == "POST":
        form = KitInstanceForm(request.POST)
        if form.is_valid():
            new_kitinstance = form.save(commit=False)
            new_kitinstance.created_date = timezone.now()
            new_kitinstance.save()
            KitInstance.objects.filter(date_added__lte=timezone.now())
            return redirect('KITS:kitinstance')
    else:
        form = KitInstanceForm()
    return render(request, 'KITS/kitinstance_add.html', {'form': form})
