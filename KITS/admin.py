from django.contrib import admin
from .models import Study, KitOrder, KitInstance, Kit


class KitInstanceInline(admin.TabularInline):
    model = KitInstance
    extra = 0

@admin.register(Kit)
class KitList(admin.ModelAdmin):
    list_display = ('IRB_number', 'type_name', 'description')
    inlines = [KitInstanceInline]


@admin.register(KitInstance)
class KitInstanceAdmin(admin.ModelAdmin):
    list_display = ('kit', 'scanner_id', 'location', 'expiration_date')
    list_filter = ('expiration_date', 'kit')
    fieldsets = (
        (None, {
            'fields': ('kit', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'expiration_date')
        }),
    )


@admin.register(KitOrder)
class KitOrderList(admin.ModelAdmin):
    list_display = ('type', 'web_address', 'description' )
    list_filter = ('type', 'web_address')
    search_fields = ('type', )
    ordering = ['type']

@admin.register(Study)
class StudyList(admin.ModelAdmin):
    list_display = ('IRB_number', 'pet_name', 'status')
    list_filter = ('IRB_number', 'start_date')
    ordering = ['IRB_number']



#test test