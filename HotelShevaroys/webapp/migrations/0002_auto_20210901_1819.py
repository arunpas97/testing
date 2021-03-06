# Generated by Django 3.1.6 on 2021-09-01 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='confom',
            name='cancel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='confom',
            name='razorpay_payment_id',
            field=models.CharField(default='None', max_length=255),
        ),
        migrations.AddField(
            model_name='reservation',
            name='cancel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservation',
            name='checkin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservation',
            name='checkin_time',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='reservation',
            name='checkout',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservation',
            name='checkout_time',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='reservation',
            name='razorpay_payment_id',
            field=models.CharField(default='None', max_length=255),
        ),
    ]
