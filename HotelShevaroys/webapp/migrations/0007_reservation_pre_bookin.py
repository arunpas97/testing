# Generated by Django 3.1.6 on 2021-09-23 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20210922_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='pre_bookIn',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
