# Generated by Django 2.2 on 2019-09-08 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brewsql', '0002_auto_20190720_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleorder',
            name='sale_order_code',
            field=models.CharField(max_length=30, null=True, unique=True, verbose_name='订单编号'),
        ),
        migrations.AlterField(
            model_name='saleorder',
            name='sale_order_date',
            field=models.DateField(null=True, verbose_name='订单日期'),
        ),
    ]
