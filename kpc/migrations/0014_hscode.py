# Generated by Django 2.0.5 on 2018-05-10 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpc', '0013_auto_20180509_0936'),
    ]

    operations = [
        migrations.CreateModel(
            name='HSCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=12)),
            ],
        ),
    ]
