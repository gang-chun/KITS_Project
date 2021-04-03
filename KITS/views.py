from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Count, Max, Q, F, Sum
from django.db.models.functions import Greatest
from django.shortcuts import render
from .filters import StudyFilter, KitFilter, KitReportFilter

from django.dispatch import receiver
from simple_history.signals import (
    pre_create_historical_record,
    post_create_historical_record
)
from datetime import datetime, timedelta


@receiver(post_create_historical_record)
def post_create_historical_record_callback(sender, **kwargs):
    t_user_t = kwargs["history_user"]

    complete_object = " ".join([str(kwargs["instance"]), str(type(kwargs["instance"]))])
    print(kwargs["history_instance"])
    date_t = kwargs["history_date"]
    viewed_on_t = models.DateTimeField(auto_now_add=True)
    # print(date_t, viewed_on_t)
    user_history_instance = \
        UserHistory.objects.create_user_history(t_user_t, complete_object, str(kwargs["history_instance"]),
                                                kwargs["history_date"])
    user_history_instance.save()
    print("Sent after saving historical record")


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
    #kit_order = KitOrder.objects.filter(study=pk)
    req = Requisition.objects.filter(study=pk)

    kit_order = KitOrder.objects.filter(study=pk)
    if kit_order.exists():
        test = 'True'
        type_qs = KitOrder.objects.filter(study=pk).values('type')
        type = type_qs[0]['type']
        kit_order = KitOrder.objects.filter(study=pk).values(type)
        kit_order = kit_order[0][type]

    else:
        test = 'False'
        kit_order ="No order details have been added"

    kit_exist = str(kits)
    if kit_exist == '<QuerySet []>':
        kit_exist = 'False'
    else:
        kit_exist = 'True'

    return render(request, 'KITS/study_detail.html', {'study': study, 'kits': kits, 'req': req, 'kit_order': kit_order, 'test':test, 'kit_exist': kit_exist})


@login_required
def study_detail_seeallkits(request, pk):
    study = get_object_or_404(Study, pk=pk)

    status = 'a or e'
    kits = KitInstance.objects.filter(kit__IRB_number=pk).filter(status__in=status).order_by('kit__id','expiration_date')

    return render(request, 'KITS/study_detail_seeallkits.html', {'study': study, 'kits': kits})

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

    test = request
    if 'study_detail' in str(test):
        test = 'study_detail'

    study = get_object_or_404(Study, pk=pk)

    if request.method == "POST":
        # update
        form = StudyForm(request.POST, instance=study)
        if form.is_valid():
            study = form.save(commit=False)
            study.updated_date = timezone.now()
            study.save()
            study = Study.objects.filter(start_date__lte=timezone.now())

            if test == 'study_detail':
                return redirect('KITS:study_detail', pk=pk)
            else:
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
def create_req(request, pk):
    study = get_object_or_404(Study, pk=pk)

    if request.method == "POST":
        form = RequisitionForm(request.POST)
        if form.is_valid():
            new_req = form.save(commit=False)
            new_req.save()
            return render(request, 'KITS/study_detail.html', {'study': study, 'new_req': new_req})
    else:
        form = RequisitionForm()
    return render(request, 'KITS/create_req.html', {'form': form, 'study': study})


@login_required
def req_edit(request, pk):
    study = get_object_or_404(Study, pk=pk)
    req = get_object_or_404(Requisition, pk=pk)

    if request.method == "POST":
        # update
        form = RequisitionForm(request.POST, instance=req)
        if form.is_valid():
            req = form.save(commit=False)
            req.updated_date = timezone.now()
            req.save()
            # req = Requisition.objects.filter(start_date__lte=timezone.now())
            return render(request, 'KITS/study_detail.html', {'study': study, 'req': req})

    else:
        # edit
        form = RequisitionForm(instance=req)
        return render(request, 'KITS/req_edit.html', {'form': form})


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

    test = request
    if 'study_detail' in str(test):
        test = 'study_detail'

    kit = get_object_or_404(Kit, pk=pk)
    if request.method == "POST":
        # update
        form = KitForm(request.POST, instance=kit)
        if form.is_valid():
            kit = form.save(commit=False)
            kit.updated_date = timezone.now()
            kit.save()
            # kit = Kit.objects.filter(start_date__lte=timezone.now())

            if test == 'study_detail':
                return redirect('KITS:study_detail', pk=kit.IRB_number_id)
            else:
                return redirect('KITS:kit_list')
    else:
        # edit
        form = KitForm(instance=kit)
    return render(request, 'KITS/kit_edit.html', {'form': form, 'kit':kit})



@login_required
def kit_delete(request, pk):
    kit = get_object_or_404(Kit, pk=pk)
    kit.delete()
    return redirect('KITS:kit_list')

# kits = Kit.objects.filter(id=pk)


@login_required
def kit_addkitinstance(request, pk):
    kit_instance = get_object_or_404(Kit, pk=pk)
    # kit_instance = Kit.objects.filter(id=pk)

    if request.method == "POST":
        form = KitInstanceForm(request.POST)
        if form.is_valid():

            # new_kitinstance = KitInstance.objects.get(form.cleaned_data['pk'])
            new_kitinstance = form.save(commit=False)
            new_kitinstance.kit_id = pk
            # new_kitinstance.created_date = timezone.now()
            new_kitinstance.kit_id = pk
            new_kitinstance.save()
            # KitInstance.objects.filter(date_added__lte=timezone.now())

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


@login_required
def report(request):
    return render(request, 'KITS/report.html')


@login_required
def report_expiredkits(request):

    today = date.today()
    in1month = today + timedelta(days=30)
    i = today.strftime('%Y-%m-%d')
    j = in1month.strftime('%Y-%m-%d')
    # KitInstance.objects.filter(expiration_date__range=(i,j)

    kits = KitInstance.objects.filter(status='e')


    # To grab the IRB numbers and put them into a list
    kits2 = list(kits)
    test = []
    test1 = []
    for kit in kits2:
        test1 = kit.kit.IRB_number
        test.append(test1)

    # To GET the IRB_number from the user's search
    myFilter = KitReportFilter(request.GET)
    test = myFilter.qs

    # To redo the 'kits' after the user searches
    kits = KitInstance.objects.filter(status='e').filter(kit__in=test)

    return render(request, 'KITS/report_expiredkits.html', {'kits': kits, 'myFilter': myFilter})


@login_required
def report_expiredkits_studies(request):
    kits = Kit.objects.filter(kit__status='e').values('IRB_number__IRB_number')\
        .annotate(qty=Count('kit')).values('IRB_number__IRB_number', 'qty', 'IRB_number__pet_name')

    return render(request, 'KITS/report_expiredkits_studies.html', {'kits': kits})


@login_required
def kit_ordering(request, pk):

    kitorder = get_object_or_404(KitOrder, pk=pk)


    if request.method == "POST":
        form = KitOrderForm(request.POST, instance=kitorder)
        if form.is_valid():
            kitorder = form.save(commit=False)
            kitorder.update_date = timezone.now()
            kitorder.save()
            return redirect('KITS:study_detail', pk=pk)

    else:
        # edit
        form = KitOrderForm(instance=kitorder)

    return render(request, 'KITS/kit_ordering.html', {'form': form})

@login_required
def kit_ordering_add(request, pk):
    #new_kitorder = get_object_or_404(Study, pk=pk)
    study = get_object_or_404(Study, pk=pk)

    if request.method == "POST":
        form = KitOrderForm(request.POST)
        if form.is_valid():
            new_kitorder = form.save(commit=False)
            new_kitorder.save()
            return redirect('KITS:study_detail', pk=pk)
    else:
        form = KitOrderForm()
    return render(request, 'KITS/kit_ordering_add.html', {'form': form, 'study':study})

@login_required
def kit_addlocation(request):

    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.created_date = timezone.now()
            location.save()
            return redirect('KITS:kit_list')
    else:
        form = LocationForm()
    return render(request, 'KITS/kit_addlocation.html', {'form': form})