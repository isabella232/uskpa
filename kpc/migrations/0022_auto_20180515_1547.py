# Generated by Django 2.0.5 on 2018-05-15 15:47

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('kpc', '0021_auto_20180515_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificateconfig',
            name='kp_countries',
            field=django_countries.fields.CountryField(blank=True, help_text='Countries available for selection as Country of Origin', max_length=746, multiple=True, verbose_name='KP Countries'),
        ),
        migrations.AddField(
            model_name='historicalcertificateconfig',
            name='kp_countries',
            field=django_countries.fields.CountryField(blank=True, help_text='Countries available for selection as Country of Origin', max_length=746, multiple=True, verbose_name='KP Countries'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='country_of_origin',
            field=django_countries.fields.CountryField(blank=True, max_length=746, multiple=True, verbose_name='Country of Origin'),
        ),
        migrations.AlterField(
            model_name='historicalcertificate',
            name='country_of_origin',
            field=django_countries.fields.CountryField(blank=True, max_length=746, multiple=True, verbose_name='Country of Origin'),
        ),
    ]
