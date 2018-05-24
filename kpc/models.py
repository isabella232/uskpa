import datetime
from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.http import QueryDict
from django.urls import reverse
from django_countries.fields import CountryField
from localflavor.us.models import USStateField, USZipCodeField
from simple_history.models import HistoricalRecords
from solo.models import SingletonModel


class CertificateConfig(SingletonModel):
    days_to_expiry = models.PositiveIntegerField(default=60)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=20.00)
    kp_countries = CountryField(multiple=True, blank=True,
                                help_text='Countries available for selection as Country of Origin',
                                verbose_name='KP Countries')

    history = HistoricalRecords()

    def __str__(self):
        return "Configuration"

    class Meta:
        verbose_name = "Certificate Configuration"
        verbose_name_plural = "Certificate Configuration"


class VoidReason(models.Model):
    value = models.CharField(max_length=500)
    sort_order = models.IntegerField(default=0)

    history = HistoricalRecords()

    class Meta:
        ordering = ['sort_order', 'value']

    def __str__(self):
        return self.value


class HSCode(models.Model):
    value = models.CharField(max_length=12)
    sort_order = models.IntegerField(default=0)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Harmonized System Code'
        ordering = ['sort_order', 'value']

    def __str__(self):
        return self.value


class PortOfExport(models.Model):
    name = models.CharField(max_length=50)
    sort_order = models.IntegerField(default=0)

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Port of Export'
        verbose_name_plural = 'Ports of Export'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Licensee(models.Model):
    """
    An entity involved in the export/import of rough diamonds
    within the United States
    """
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=1024)
    address2 = models.CharField(verbose_name='Address continued',
                                max_length=1024, blank=True)
    city = models.CharField(max_length=1024)
    state = USStateField()
    zip_code = USZipCodeField()
    tax_id = models.CharField(max_length=10,
                              help_text='Tax Identification Number',
                              validators=[
                                  RegexValidator(regex='\d{2}-\d{7}',
                                                 message='TIN format: ##-#######'
                                                 )
                              ]
                              )
    is_active = models.BooleanField(default=True, help_text="Licensee is active - able to request and access certificates")
    history = HistoricalRecords()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('licensee', args=[self.id])

    def user_can_access(self, user):
        return user.is_superuser or user.profile.is_auditor or \
            user.profile.licensees.filter(id=self.id).exists()

    @property
    def address_text(self):
        """compose address fields into text block"""
        address = self.address
        if self.address2:
            address += f'\n{self.address2}'
        address += f"\n{self.city}, {self.state} {self.zip_code}"
        address += '\nUnited States of America'
        return address


class KpcAddress(models.Model):
    """Common address used by licensees when completing Certificates"""
    name = models.CharField(max_length=256)
    address = models.TextField()
    country = CountryField()
    licensee = models.ForeignKey(Licensee, related_name='addresses', on_delete=models.PROTECT)

    class Meta:
        unique_together = ('licensee', 'name',)
        ordering = ['licensee', 'name', ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('addressee', args=[self.id])

    def get_delete_url(self):
        return reverse('addressee-delete', args=[self.id])


class Receipt(models.Model):
    number = models.IntegerField(default=settings.LAST_RECEIPT_NUMBER, unique=True)
    licensee_name = models.CharField(max_length=256)
    licensee_address = models.TextField()
    certificates = ArrayField(models.CharField(max_length=32))
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    certificates_sold = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=256)
    contact = models.CharField(max_length=256)
    date_sold = models.DateField()

    history = HistoricalRecords()

    class Meta:
        ordering = ['-number']

    def save(self, *args, **kwargs):
        """Auto-increment number"""
        if not self.id:
            last_receipt = Receipt.objects.first()
            if last_receipt:
                self.number = last_receipt.number + 1
        super().save(*args, **kwargs)

    @classmethod
    def from_registration_form(cls, form):
        receipt = cls()
        receipt.licensee_name = form.cleaned_data['licensee'].name
        receipt.licensee_address = form.cleaned_data['licensee'].address_text
        receipt.certificates = [f'US{num}' for num in form.get_cert_list()]
        receipt.total_paid = form.cleaned_data['payment_amount']
        receipt.certificates_sold = len(receipt.certificates)
        receipt.unit_price = CertificateConfig.get_solo().price
        receipt.payment_method = form.cleaned_data['payment_method']
        receipt.contact = form.cleaned_data['contact'].profile.get_user_display_name()
        receipt.date_sold = form.cleaned_data['date_of_sale']
        return receipt

    def __str__(self):
        return f'Receipt ({self.number})'

    def get_absolute_url(self):
        return reverse('receipt', args=[self.id])

    @property
    def certificates_text(self):
        return ', '.join(self.certificates)


class Certificate(models.Model):
    AVAILABLE = 0
    PREPARED = 1
    SHIPPED = 2
    DELIVERED = 3
    VOID = 4

    DEFAULT_SEARCH = [AVAILABLE, PREPARED, SHIPPED]
    DEFAULT_AUDITOR_SEARCH = [PREPARED, SHIPPED, DELIVERED]
    MODIFIABLE_STATUSES = [PREPARED, SHIPPED]

    STATUS_CHOICES = (
        (AVAILABLE, 'Available'),
        (PREPARED, 'Prepared'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (VOID, 'Void')
    )

    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('check', 'Check'),
    )

    # Fields on physical certificate
    PHYSICAL_FIELDS = ('number', 'country_of_origin', 'aes', 'date_of_issue', 'date_of_expiry',
                       'shipped_value', 'exporter', 'exporter_address', 'number_of_parcels',
                       'consignee', 'consignee_address', 'carat_weight', 'harmonized_code__value')

    number = models.PositiveIntegerField(
        help_text='USKPA Certificate ID number', unique=True)
    aes = models.CharField(max_length=30,
                           blank=True,
                           help_text='AES Confirmation Number (ITN)',
                           verbose_name='AES',
                           validators=[
                               RegexValidator(regex='X\d{14}',
                                              message='AES Confirmation (ITN) format is 14 digits prepended by X: X##############'
                                              )
                           ]
                           )
    country_of_origin = CountryField(blank=True, verbose_name='Country of Origin')
    date_of_issue = models.DateField(
        blank=True, null=True, help_text='Date of Issue')
    date_of_expiry = models.DateField(blank=True, null=True)
    shipped_value = models.DecimalField(max_digits=20, decimal_places=2,
                                        blank=True, null=True, help_text="Value in USD",
                                        validators=[MinValueValidator(Decimal(0.009),
                                                                      message='Shipped value must be greater than 0')
                                                    ]
                                        )
    exporter = models.CharField(blank=True, max_length=256)
    exporter_address = models.TextField(blank=True)
    number_of_parcels = models.PositiveIntegerField(blank=True, null=True)
    consignee = models.CharField(blank=True, max_length=256)
    consignee_address = models.TextField(blank=True)
    carat_weight = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True,
                                       validators=[MinValueValidator(Decimal(0.009),
                                                                     message='Carat weight must be at least 0.01')
                                                   ]
                                       )
    harmonized_code = models.ForeignKey(HSCode, blank=True, null=True, on_delete=models.PROTECT)

    # Non certificate fields
    port_of_export = models.ForeignKey(
        PortOfExport, blank=True, null=True, on_delete=models.PROTECT)
    assignor = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT)
    licensee = models.ForeignKey(
        'Licensee', blank=True, null=True, on_delete=models.PROTECT)
    status = models.IntegerField(choices=STATUS_CHOICES, default=AVAILABLE)
    last_modified = models.DateTimeField(blank=True, editable=False)
    date_of_sale = models.DateField(
        blank=True, null=True, help_text='Date of sale to licensee')
    payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICES, max_length=5,
                                      blank=True)
    void = models.BooleanField(
        default=False, help_text="Certificate has been voided?")
    notes = models.TextField(blank=True)

    attested = models.BooleanField(default=False, help_text="""I have completed the necessary
                                                                application pertaining to this shipment,
                                                                including the warranty that the diamonds
                                                                being shipped were not traded to fund conflict.""")
    date_of_shipment = models.DateField(
        blank=True, null=True, help_text='Date certificate was marked SHIPPED')
    date_of_delivery = models.DateField(
        blank=True, null=True, help_text='Date certificate was marked DELIVERED')
    date_voided = models.DateField(
        blank=True, null=True, help_text="Date on which this certificate was voided")
    history = HistoricalRecords()

    class Meta:
        get_latest_by = ('number', )

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        """
        Update last_modified if object already exists
        Or we're creating a new object and not setting it ourselves
        """
        if self.id or not self.last_modified:
            self.last_modified = datetime.datetime.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('cert-details', args=[self.number])

    def get_anchor_tag(self):
        """Link to this object"""
        return f"<a href={self.get_absolute_url()}>{self.display_name}</a>"

    @property
    def display_name(self):
        return f"US{self.number}"

    @classmethod
    def next_available_number(cls):
        """Starting point for new certificate ID generation"""
        try:
            return cls.objects.latest().number + 1
        except cls.DoesNotExist:
            return 1

    @classmethod
    def default_search_filters(cls, user):
        """Return default search as URL parameters"""
        q = QueryDict(mutable=True)
        if user.profile.is_auditor:
            q.setlist('status', cls.DEFAULT_AUDITOR_SEARCH)
        else:
            q.setlist('status', cls.DEFAULT_SEARCH)
        return q.urlencode()

    @property
    def licensee_editable(self):
        return self.status == self.AVAILABLE

    @property
    def status_can_be_updated(self):
        """Certificate may be modified by users?"""
        return self.status in self.MODIFIABLE_STATUSES

    @property
    def next_status_label(self):
        """Return label of next status"""
        if self.status in self.MODIFIABLE_STATUSES:
            return dict(self.STATUS_CHOICES)[self.status+1]

    @property
    def next_status_value(self):
        """Return value of next status"""
        if self.status in self.MODIFIABLE_STATUSES:
            return self.status+1

    def user_can_access(self, user):
        """True if user can access this certificate"""
        return user.profile.certificates().filter(id=self.id).exists()

    def user_can_edit(self, user):
        return self.user_can_access(user) and not user.profile.is_auditor

    @classmethod
    def get_label_for_status(cls, status):
        return dict(cls.STATUS_CHOICES).get(status)

    @staticmethod
    def get_price():
        return CertificateConfig.get_solo().price

    @staticmethod
    def get_expiry_days():
        return CertificateConfig.get_solo().days_to_expiry

    @staticmethod
    def get_void_reasons():
        return VoidReason.objects.all()
