# Generated by Django 2.2.13 on 2020-08-11 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewsql', '0004_auto_20200809_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='brew',
            name='volume_in',
            field=models.IntegerField(blank=True, null=True, verbose_name='入罐容量'),
        ),
    ]
