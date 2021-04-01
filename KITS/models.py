from django.utils import timezone
from django.contrib.auth.models import User  # So we can test if authenticated
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from datetime import date, timedelta
from django.db import models
from simple_history.models import HistoricalRecords
import uuid  # Required for unique study instances


# Create your models here.

class KitOrder(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=100, blank=True)
    web_address = models.URLField(max_length=200, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.type)


class Study(models.Model):
    id = models.AutoField(primary_key=True)
    kit_order = models.ForeignKey(KitOrder, on_delete=models.CASCADE, related_name='kit_orders')
    IRB_number = models.CharField(max_length=50)
    pet_name = models.CharField(max_length=50)
    comment = models.CharField(max_length=100, blank=True)
    sponsor_name = models.CharField(max_length=100)
    requisition_form_qty = models.CharField(max_length=5)
    history = HistoricalRecords()
    STATUS = (
        ('Preparing to Open', 'Preparing to Open'),
        ('Open', 'Open'),
        ('Closed', 'Closed')
    )

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default='Preparing to Open',
    )

    start_date = models.DateTimeField(
        default=timezone.now)
    # auto_now_add=True
    end_date = models.DateTimeField(blank=True)

    class Meta:
        ordering = ['IRB_number']
        verbose_name_plural = "Studies"

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.IRB_number)


class Location(models.Model):
    building = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    shelf_number = models.CharField(max_length=100, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'{self.building} ({self.room})'


class Kit(models.Model):
    IRB_number = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='studies')
    description = models.CharField(max_length=100, blank=True)
    date_added = models.DateTimeField(
        default=timezone.now)
    type_name = models.CharField(max_length=32, blank=True)
    # history = HistoricalRecords()

    def __str__(self):
        return f'{self.IRB_number} ({self.type_name})'


class KitInstance(models.Model):
    """Model representing a specific kit (i.e. that can be used by a Study).
    If a scanner_id generated by bar code scanner, then scanner_id will override default"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular kit used in any Study')
    scanner_id = models.CharField(max_length=100)
    kit = models.ForeignKey('Kit', on_delete=models.RESTRICT, related_name='kit')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location')

    note = models.CharField(max_length=100, blank=True)

    expiration_date = models.DateField(null=True, blank=True)
    KIT_STATUS = (
        ('a', 'Available'),
        ('c', 'Checked Out'),
        ('e', 'Expired'),
        ('d', 'Demolished'),
    )

    status = models.CharField(
        max_length=1,
        choices=KIT_STATUS,
        blank=True,
        default='a',
        help_text='Kit Availability',
    )
    # history = HistoricalRecords()

    class Meta:
        ordering = ['expiration_date']
        permissions = (("can_mark_demolished", "Set kit as demolished"),)

    @property
    def is_expired(self):
        if date.today() > self.expiration_date:
            return True
        return False

    @property
    def expired_soon(self):
        if date.today() > self.expiration_date + timedelta(days=3):
            return True
        return False

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.kit}) {self.status} {self.expiration_date}'


class Requisition(models.Model):
    id = models.AutoField(primary_key=True)
    study = models.ForeignKey(Study, on_delete=models.CASCADE, null=True, blank=True)
    link = models.URLField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, default='TBD')
    file = models.FileField(blank=True, null=True, upload_to='req/')

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    # history = HistoricalRecords()


class UserHistoryManager(models.Manager):
    def create_user_history(self, user, the_object, changed_on, history_instance):
        user_hisx = self.create(user=user, the_object=the_object, changed_on=changed_on,
                                history_instance=history_instance)
        # do something with the user_hisx object if needed
        return user_hisx


class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    the_object = models.CharField(max_length=100, blank=False)
    history_instance = models.CharField(max_length=100, blank=False)
#    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
#    object_id = models.PositiveIntegerField() # 1, 2, ...
#    content_object = GenericForeignKey()  # Exact names used so no need to pass 'obj_id', 'cont_obj' in ctor
    changed_on = models.DateTimeField(auto_now_add=True)
    objects = UserHistoryManager()

    def __str__(self):
        return str(self.history_instance + self.the_object)

    class Meta:
        verbose_name_plural = "UserHistories"
