"""
    Example Admin Site. See the following reference to customize the admin site:
    https://realpython.com/customize-django-admin-python/
    This page contains a number of examples of how to customize the admin according to your needs.
"""

from django.contrib import admin
from django.urls import reverse
from .models import Contact, CustomerAccount, Supplier, Part, Service, CustomerLocation, HardwareVersion, SoftwareVersion, \
    Device, DeviceData
from django.utils.html import format_html


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contact Model
    """
    # Example list_display shows the fields that will render on the top level Contacts page
    list_display = ("last_name", "first_name", "phone_number", "email_address", "date_added")

    # Example of how to separate fields into fieldsets with header information for each fieldset
    fieldsets = [
        ('Contact Information', {'fields': ['first_name', "last_name", "phone_number", "email_address"]}),
        ('Date Information', {'fields': ['date_added']}),
    ]

    # Example of creating a search bar
    search_fields = ("last_name__startswith",)


@admin.register(CustomerAccount)
class CustomerAccountAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CustomerAccount model
    """
    list_display = ("name", "sales_contact", "get_contact_number" )

    # Example of a generated list_display field
    def get_contact_number(self, obj):
        return obj.sales_contact.phone_number


@admin.register(CustomerLocation)
class CustomerLocationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the CustomerLocation model
    """
    list_display = ("partner", "address", "installation_contact", "install_contact_number")

    def install_contact_number(self, obj):
        return obj.installation_contact.phone_number


@admin.register(HardwareVersion)
class HardwareVersionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the HardwareVersion model
    """
    list_display = ("name", "version")


@admin.register(SoftwareVersion)
class SoftwareVersionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the SoftwareVersion model
    """
    list_display = ("name", "version")


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Device model
    """
    list_display = ("serial_number", "model", "software", "register_date", "location_link")
    list_filter = ("model",)

    # Example fields element shows the fields in this order when you select a customer account
    fields = ["model", "software", "serial_number", "register_date"]

    # Example of creating a custom link to a foreign key as part of the list_display fields in the admin page.
    def location_link(self, obj):
        # Get it to point to a link to the location
        url = (
            reverse(f"admin:blueprint_customerlocation_change", args=(obj.id,))
        )
        location = obj.location
        return format_html('<a href="{}">{}</a>', url, location)


@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    """
    Admin configuration for the DeviceData model
    """
    list_display = ("datetime", "device_link", "cpu", "memory")

    def device_link(self, obj):
        # Get it to point to a link to the device
        url = (
            reverse(f"admin:manager_devicedata_change", args=(obj.id,))
        )
        device = obj.device
        return format_html('<a href="{}">{}</a>', url, device)


# Examples with no customization of the admin panel.
admin.site.register(Supplier)
admin.site.register(Part)
admin.site.register(Service)


