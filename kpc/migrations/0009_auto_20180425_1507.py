# Generated by Django 2.0.4 on 2018-04-25 15:07

import django.core.validators
from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kpc', '0008_auto_20180419_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='aes',
            field=models.CharField(blank=True, help_text='AES Confirmation Number (ITN)', max_length=15, validators=[django.core.validators.RegexValidator(message='AES Confirmation (ITN) format is 14 digits prepended by X: X##############', regex='X\\d{14}')], verbose_name='AES'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='country_of_origin',
            field=django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='Country of Origin'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='date_of_expiry',
            field=models.DateField(blank=True, help_text='Date of Expiry', null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='date_of_issue',
            field=models.DateField(blank=True, help_text='Date of Issue', null=True),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='date_of_sale',
            field=models.DateField(blank=True, help_text='Date of sale to licensee', null=True),
        ),
        migrations.AlterField(
            model_name='historicalcertificate',
            name='aes',
            field=models.CharField(blank=True, help_text='AES Confirmation Number (ITN)', max_length=15, validators=[django.core.validators.RegexValidator(message='AES Confirmation (ITN) format is 14 digits prepended by X: X##############', regex='X\\d{14}')], verbose_name='AES'),
        ),
        migrations.AlterField(
            model_name='historicalcertificate',
            name='country_of_origin',
            field=django_countries.fields.CountryField(blank=True, max_length=2, verbose_name='Country of Origin'),
        ),
        migrations.AlterField(
            model_name='historicalcertificate',
            name='date_of_expiry',
            field=models.DateField(blank=True, help_text='Date of Expiry', null=True),
        ),
        migrations.AlterField(
            model_name='historicalcertificate',
            name='date_of_issue',
            field=models.DateField(blank=True, help_text='Date of Issue', null=True),
        ),
        migrations.AlterField(
            model_name='historicalcertificate',
            name='date_of_sale',
            field=models.DateField(blank=True, help_text='Date of sale to licensee', null=True),
        ),
    ]