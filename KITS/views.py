from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.db.models import Count, Max, Q
# from django.db.models import F, Sum
# from django.db.models.functions import Greatest
from .filters import StudyFilter, KitFilter, KitReportFilter, KitInstanceFilter


from django.dispatch import receiver
from simple_history.signals import (
    pre_create_historical_record,
    post_create_historical_record
)
from datetime import datetime, timedelta
from django.contrib import messages


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


def list_history(request):
    header = "Action Key: +=created ~=changed"
    queryset = KitInstance.objects.raw("SELECT * FROM KITS_historicalkitinstance")
    context = {
        "header": header,
        "queryset": queryset,
    }
    return render(request, "KITS/list_history.html", context)

@login_required
def study_list(request):
    studies = Study.objects.exclude(status='Closed')

    # Filter bar
    study_filter = StudyFilter(request.GET, queryset=Study.objects.all())
    if request.GET:
        studies = study_filter.qs

    return render(request, 'KITS/study_list.html', {'studies': studies, 'study_filter': study_filter})


@login_required
def study_detail(request, pk):
    study = get_object_or_404(Study, pk=pk)

    kits = Kit.objects.filter(IRB_number=pk).annotate(
        no_of_kits=Count('kit', filter=Q(kit__status='a'))) \
        .annotate(no_of_kits_exp=Count('kit', filter=Q(kit__status='e'))) \
        .annotate(exp=Max('kit__expiration_date'))

    req = Requisition.objects.filter(study=pk)
    if req.exists():
        req_exist = True
        type_qs = Requisition.objects.filter(study=pk).values('type')
        type_list = type_qs[0]['type']
        req = Requisition.objects.filter(study=pk).values(type_list)
        req = req[0][type_list]
    else:
        req_exist = False
        req = 'No requisition details have been added.'

    kit_order = KitOrder.objects.filter(study=pk)
    if kit_order.exists():
        test = 'True'
        type_qs = KitOrder.objects.filter(study=pk).values('type')
        type_list = type_qs[0]['type']
        kit_order = KitOrder.objects.filter(study=pk).values(type_list)
        kit_order = kit_order[0][type_list]

    else:
        test = 'False'
        kit_order = "No order details have been added."

    kit_exist = str(kits)
    if kit_exist == '<QuerySet []>':
        kit_exist = 'False'
    else:
        kit_exist = 'True'

    return render(request, 'KITS/study_detail.html', {'study': study, 'kits': kits, 'req': req, 'kit_order': kit_order,
                                                      'test': test, 'kit_exist': kit_exist, 'req_exist': req_exist})


@login_required
def study_detail_seeallkits(request, pk):
    study = get_object_or_404(Study, pk=pk)

    status = 'a or e'
    kits = KitInstance.objects.filter(kit__IRB_number=pk).filter(status__in=status).order_by('kit__id',
                                                                                             'expiration_date')

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

    # To redirect to the study details page if the request came from the study details page
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

    message = "The study's status has changed to 'closed' and was put into archive."
    messages.success(request, message)
    return redirect('KITS:study_list')


@login_required
def create_req(request, pk):

    study = get_object_or_404(Study, pk=pk)

    if request.method == "POST":
        form = RequisitionForm(request.POST, request.FILES)
        if form.is_valid():
            new_req = form.save(commit=False)
            new_req.save()
            return redirect('KITS:study_detail', pk=pk)
    else:
        form = RequisitionForm()
    return render(request, 'KITS/create_req.html', {'form': form, 'study': study})


@login_required
def req_edit(request, pk):
    req = get_object_or_404(Requisition, pk=pk)

    if request.method == "POST":
        form = RequisitionForm(request.POST, request.FILES, instance=req)
        if form.is_valid():
            req = form.save(commit=False)
            req.update_date = timezone.now()
            req.save()
            return redirect('KITS:study_detail', pk=pk)
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
    kit = Kit.objects.exclude(IRB_number__status='Closed')
    # Filter bar
    kit_filter = KitFilter(request.GET, queryset=kit)
    kit = kit_filter.qs

    return render(request, 'KITS/kit_list.html', {'kit': kit, 'kit_filter': kit_filter})


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
    return render(request, 'KITS/kit_edit.html', {'form': form, 'kit': kit})


@login_required
def kit_delete(request, pk):
    try:
        kit = get_object_or_404(Kit, pk=pk)
        kit.delete()
    except:
        message = "This kit type cannot be deleted because there are kits still in inventory."
        messages.error(request, message)
        return redirect('KITS:kit_list')

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
    kit_report_filter = KitReportFilter(request.GET)
    test = kit_report_filter.qs

    # To redo the 'kits' after the user searches
    kits = KitInstance.objects.filter(status='e').filter(kit__in=test)

    return render(request, 'KITS/report_expiredkits.html', {'kits': kits, 'kit_report_filter': kit_report_filter})


@login_required
def report_expiredkits_studies(request):
    kits = Kit.objects.filter(kit__status='e').values('IRB_number__IRB_number')\
        .annotate(qty=Count('kit')).values('IRB_number__IRB_number', 'qty', 'IRB_number__pet_name')

    return render(request, 'KITS/report_expiredkits_studies.html', {'kits': kits})


@login_required
def kit_ordering(request, pk):

    kitorder = get_object_or_404(KitOrder, pk=pk)

    if request.method == "POST":
        form = KitOrderForm(request.POST, request.FILES, instance=kitorder)
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
    # new_kitorder = get_object_or_404(Study, pk=pk)
    study = get_object_or_404(Study, pk=pk)

    if request.method == "POST":
        form = KitOrderForm(request.POST, request.FILES)
        if form.is_valid():
            new_kitorder = form.save(commit=False)
            new_kitorder.save()
            return redirect('KITS:study_detail', pk=pk)
    else:
        form = KitOrderForm()
    return render(request, 'KITS/kit_ordering_add.html', {'form': form, 'study': study})


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


@login_required
def kit_checkout(request):
    kitinstance = KitInstance.objects.all()
    # Filter bar
    kit_instance_filter = KitInstanceFilter(request.GET, queryset=kitinstance)
    kitinstance = kit_instance_filter.qs
    return render(request, 'KITS/kit_checkout.html', {'kitinstance': kitinstance,
                                                      'kit_instance_filter': kit_instance_filter})


@login_required
def help(request):
    return render(request, 'KITS/help.html')




@login_required
def kitinstance_statusedit(request,pk):
    kit = get_object_or_404(KitInstance, pk=pk)
    kitinstance = KitInstance.objects.all()
    #kit = get_object_or_404(KitInstance.objects.values('kit__id'), pk=pk)
    if request.method == "POST":
        form = KitInstanceEditForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_date = timezone.now()
            instance.save()
            #form.save()
        return redirect('KITS:kit_checkout')
    else:
        form = KitInstanceEditForm()

    return render(request, 'KITS/kitinstance_statusedit.html', {'kit': kit, 'form': form, 'kitinstance': kit})




@login_required
def kitinstance_demolish(request,pk):
    kit = get_object_or_404(KitInstance, pk=pk)
    kitinstance = KitInstance.objects.all()
    #kit = get_object_or_404(KitInstance.objects.values('kit__id'), pk=pk)
    if request.method == "POST":
        form = KitInstanceDemolishForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_date = timezone.now()
            instance.save()
            #form.save()
        return redirect('KITS:kit_checkout')
    else:
        form = KitInstanceDemolishForm()

    return render(request, 'KITS/kitinstance_demolish.html', {'kit': kit, 'form': form, 'kitinstance': kit})


