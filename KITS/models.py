from django.utils import timezone
from django.contrib.auth.models import User  # So we can test if authenticated
from datetime import date
from django.db import models
import uuid  # Required for unique study instances


# Create your models here.

class KitOrder(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=100, blank=True)
    web_address = models.URLField(max_length=200, blank=True)

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
    # status = models.CharField(max_length=100)
    STATUS = (
        ('Preparing to Open', ('Preparing to Open')),
        ('Open', ('Open')),
        ('Closed', ('Closed'))
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

    def __str__(self):
        return f'{self.building} ({self.room})'


class Kit(models.Model):
    IRB_number = models.ForeignKey(Study, on_delete=models.CASCADE, related_name='studies')
    type_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.IRB_number} ({self.type_name})'


class KitInstance(models.Model):
    """Model representing a specific kit (i.e. that can be used by a Study).
    If a scanner_id generated by bar code scanner, then scanner_id will override default"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular kit used in any Study')
    scanner_id = models.CharField(max_length=100, default=id)
    kit = models.ForeignKey('Kit', on_delete=models.RESTRICT)
    Location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='location')

    location = models.CharField(max_length=100)

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

    class Meta:
        ordering = ['expiration_date']
        permissions = (("can_mark_demolished", "Set kit as demolished"),)

    @property
    def is_expired(self):
        if date.today() > self.expiration_date:
            return True
        return False

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.kit}) {self.status} {self.expiration_date}'
