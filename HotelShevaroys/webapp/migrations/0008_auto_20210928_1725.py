# Generated by Django 3.1.6 on 2021-09-28 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_reservation_pre_bookin'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='img2',
            field=models.ImageField(blank=True, null=True, upload_to='rooms/'),
        ),
        migrations.AddField(
            model_name='room',
            name='img3',
            field=models.ImageField(blank=True, null=True, upload_to='rooms/'),
        ),
        migrations.AddField(
            model_name='room',
            name='img4',
            field=models.ImageField(blank=True, null=True, upload_to='rooms/'),
        ),
        migrations.AddField(
            model_name='room',
            name='max_price_date1',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='room',
            name='max_price_date2',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='room',
            name='price2',
            field=models.CharField(blank=True, default='None', max_length=10),
        ),
        migrations.AlterField(
            model_name='room',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='rooms/'),
        ),
    ]
