# Generated by Django 2.0.4 on 2018-04-16 23:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kpc', '0003_auto_20180416_2036'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(help_text='USKPA Certificate ID number')),
                ('aes', models.CharField(blank=True, help_text='AES Confirmation Number (ITN)', max_length=15, validators=[django.core.validators.RegexValidator(message='AES Confirmation (ITN) format: X##############', regex='X\\d{14}')])),
                ('country_of_origin', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('date_of_issue', models.DateTimeField(blank=True, help_text='Date of Issue', null=True)),
                ('date_of_expiry', models.DateTimeField(blank=True, help_text='Date of Expiry', null=True)),
                ('shipped_value', models.DecimalField(blank=True, decimal_places=2, help_text='Value in U.S. $', max_digits=20, null=True)),
                ('exporter', models.CharField(blank=True, max_length=256)),
                ('exporter_address', models.TextField(blank=True)),
                ('number_of_parcels', models.PositiveIntegerField(blank=True, null=True)),
                ('consignee', models.CharField(blank=True, help_text='Ultimate Consignee Name', max_length=256)),
                ('consignee_address', models.TextField(blank=True, help_text='Ultimate Consignee Address')),
                ('carat_weight', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_of_sale', models.DateTimeField(blank=True, help_text='Date of sale to licensee', null=True)),
                ('void', models.BooleanField(default=False, help_text='Certificate has been voided')),
                ('notes', models.TextField(blank=True)),
                ('assignor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': ('number',),
            },
        ),
        migrations.CreateModel(
            name='DeliveryStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('label', models.CharField(max_length=32)),
                ('sort_order', models.IntegerField(default=0, help_text='Sort order override for select inputs')),
            ],
            options={
                'verbose_name_plural': 'Delivery statuses',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCertificate',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('number', models.PositiveIntegerField(help_text='USKPA Certificate ID number')),
                ('aes', models.CharField(blank=True, help_text='AES Confirmation Number (ITN)', max_length=15, validators=[django.core.validators.RegexValidator(message='AES Confirmation (ITN) format: X##############', regex='X\\d{14}')])),
                ('country_of_origin', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('date_of_issue', models.DateTimeField(blank=True, help_text='Date of Issue', null=True)),
                ('date_of_expiry', models.DateTimeField(blank=True, help_text='Date of Expiry', null=True)),
                ('shipped_value', models.DecimalField(blank=True, decimal_places=2, help_text='Value in U.S. $', max_digits=20, null=True)),
                ('exporter', models.CharField(blank=True, max_length=256)),
                ('exporter_address', models.TextField(blank=True)),
                ('number_of_parcels', models.PositiveIntegerField(blank=True, null=True)),
                ('consignee', models.CharField(blank=True, help_text='Ultimate Consignee Name', max_length=256)),
                ('consignee_address', models.TextField(blank=True, help_text='Ultimate Consignee Address')),
                ('carat_weight', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('last_modified', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_of_sale', models.DateTimeField(blank=True, help_text='Date of sale to licensee', null=True)),
                ('void', models.BooleanField(default=False, help_text='Certificate has been voided')),
                ('notes', models.TextField(blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('assignor', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical certificate',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalHSCode',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical HS code',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HSCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': 'HS code',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField()),
                ('label', models.CharField(max_length=32)),
                ('sort_order', models.IntegerField(default=0, help_text='Sort order override for select inputs')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='historicalcertificate',
            name='harmonized_code',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='kpc.HSCode'),
        ),
        migrations.AddField(
            model_name='historicalcertificate',
            name='history_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='historicalcertificate',
            name='licensee',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='kpc.Licensee'),
        ),
        migrations.AddField(
            model_name='historicalcertificate',
            name='payment_method',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='kpc.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='historicalcertificate',
            name='status',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='kpc.DeliveryStatus'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='harmonized_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kpc.HSCode'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='licensee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kpc.Licensee'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kpc.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='kpc.DeliveryStatus'),
        ),
    ]