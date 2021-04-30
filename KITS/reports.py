from .models import *
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta, date
from .datavisualization import get_month, get_year
from django.db.models import Count, Q


def query_active_studies(startdate, enddate):
    qs = KitInstance.objects.values('id', 'created_date', 'status')

    list = []

    #Iterate through each kit instance to check if the date created is within date range
    for q in qs:

        #If kit instance was created within date range, add to the list
        if check_date(q['created_date'], startdate, enddate) == True:
            list.append((q['id'], q['created_date'], 'added'))

        # Check if a kit instance had a status change
        kit_inst = historical_status_change(q['id'])

        if kit_inst is not None:
            # If historical_status_change returns with values (i.e. not None)
            # Then check the date of that status change
            if check_date(kit_inst[1], startdate, enddate) == True:

                # If status change within date range
                if kit_inst[0] == 'demolished':
                    list.append((q['id'], kit_inst[1], 'demolished'))
                elif kit_inst[0] == 'checked-out':
                    list.append((q['id'], kit_inst[1], 'checked_out'))

    outfile = "kitactivity.csv"
    file = open(outfile, 'w')
    file.write("ID,Date,Action\n")
    for entry in list:
        id, date, action = entry
        month = get_month(date)
        year = get_year(date)
        file.write(str(id) + "," + str(month) + "-" + str(year) + "," + action + "\n")
    file.close()
    return outfile

# To check each historical event for a status change for each kit instance event
# If there is a status change, return new status (i.e. demolished or checked out)
# & the date the status change occurred
def historical_status_change(id):

    #Get the one kit instance objects
    kit = get_object_or_404(KitInstance, pk=id)

    # Then get all of the historical events associated with that object
    kit = kit.history.all()

    # Iterate through all the historical instances for that specific kit instance
    for i in range(len(kit) - 1):
        delta = kit[i].diff_against(kit[i+1])
        # Compare two historical kit instances at a time and find the one where status field changed
        for change in delta.changes:
            if change.field == 'status':
                if change.new == 'd':
                    event = 'demolished'
                elif change.new == 'c':
                    event = 'checked-out'
                else:
                    return False

                # Get the date of the kit instance history status change
                hist = kit[i+1].history_date
                date = datetime.date(hist)

                return [event, date]

# Check if date falls between the start and end date
def check_date(date, startdate, enddate):

    if date > startdate and date < enddate:
        return True
    else:
        return False


def validate_date(startdate, enddate):
    if startdate == '':
        message = "Please enter in a start date"
        return message
    elif enddate == '':
        message = "Please enter in an end date"
        return message
    try:
        format = "%m-%d-%Y"
        startdate = datetime.strptime(startdate, format)
        enddate = datetime.strptime(enddate, format)
        return True
    except ValueError:
        message = "Please format date entries correctly to MM-DD-YYYY"
        return message


def query_checked_out_kits(startdate, enddate):

    checked_out = KitInstance.objects.filter(status='c')

    checkedout_kits = Kit.objects.annotate(kiti_count=Count('kit', filter=Q(kit__status='c'))).filter()

    test = []
    studies = []


    for kit in checked_out:
        if check_date(kit.checked_out_date, startdate, enddate) == False:
            break
        elif check_date(kit.checked_out_date, startdate, enddate) == True:

            study = str(kit.kit.IRB_number)

            # If the kit type belongs to a study that was already added in the list
            if study in studies:
                # Find the index value from the studies list
                study = str(kit.kit.IRB_number)
                index = studies.index(study)
                # Add checked out kits to the right IRB
                test[index][2] = 1 + int(test[index][2])

            elif study not in studies:
                studies.append(str(kit.kit.IRB_number))
                t = []
                t.append(str(kit.kit.IRB_number))
                study = get_object_or_404(Study, IRB_number=kit.kit.IRB_number)
                t.append(str(study.pet_name))
                t.append(1)
                test.append(t)

    return test
