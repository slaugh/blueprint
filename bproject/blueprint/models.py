"""
Django Models File
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Contact(models.Model):
    """
    Represents a person associated with the company. This is a contact seperate from Django's user model.
    See the following reference for more information on when to extend django's user model:
    https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email_address = models.CharField(max_length=100)
    date_added = models.DateTimeField('date added')

    def __str__(self):
        # __str__ returns a formatted string representing the model in the admin page, etc.
        return f"{self.last_name}, {self.first_name}"

    class Meta:
        # Meta defines how elements will be appear in the admin page
        ordering = ("date_added",)


class CustomerAccount(models.Model):
    """
    Represents a partner that has an account with the business.
    """
    name = models.CharField(max_length=200)
    sales_contact = models.ForeignKey(Contact, related_name='salescontact', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Supplier(models.Model):
    """
    Represents a supplier of goods or services
    """
    name = models.CharField(max_length=200)
    supply_contact = models.ForeignKey(Contact, related_name='supplycontact', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Part(models.Model):
    """
    Represents a part that is provided by a supplier
    """
    name = models.CharField(max_length=200)
    supplier = models.ForeignKey(Supplier, related_name='part', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Service(models.Model):
    """
    Represents a service that is provided by a supplier
    """
    name = models.CharField(max_length=200)
    supplier = models.ForeignKey(Supplier, related_name='service', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class CustomerLocation(models.Model):
    """
    Represents the a physical location associated with a PartnerAccount
    """
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    partner = models.ForeignKey(CustomerAccount, related_name='location', on_delete=models.CASCADE)
    installation_contact = models.ForeignKey(Contact, related_name='installation_contact', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address}"


class HardwareVersion(models.Model):
    """
    Represents a version of a hardware platform
    """
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}, {self.version}"

    class Meta:
        ordering = ("-version",)


class SoftwareVersion(models.Model):
    """
    Represents a version of a software system
    """
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.version}"


class Device(models.Model):
    """
    Represents a device instance
    """
    serial_number = models.CharField(max_length=200)
    model = models.ForeignKey(HardwareVersion, related_name='hardwareversion', on_delete=models.CASCADE)
    software = models.ForeignKey(SoftwareVersion, related_name='device', on_delete=models.CASCADE)
    register_date = models.DateTimeField('date registered')
    location = models.ForeignKey(CustomerLocation, related_name='device', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.serial_number}, {self.location}"

    class Meta:
        # Example showing how to specify that a field should be unique.
        constraints = [
            models.UniqueConstraint(fields=['serial_number'], name='unique serial_number')
        ]


class DeviceData(models.Model):
    """
    Represents data submitted by a device
    """
    datetime = models.DateTimeField()
    device = models.ForeignKey(Device, related_name='data', on_delete=models.CASCADE)
    cpu = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)])
    memory = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(1)])

    def __str__(self):
        return f"CPU: {self.cpu}, Mem: {self.memory}"

    class Meta:
        # Example showing how to represent a plural field
        verbose_name_plural = "Data"
