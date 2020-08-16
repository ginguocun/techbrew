# Generated by Django 2.2.13 on 2020-08-16 03:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brewsql', '0005_brew_volume_in'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='company_share',
        ),
        migrations.AddField(
            model_name='company',
            name='contact',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='联系人'),
        ),
        migrations.AddField(
            model_name='saleorder',
            name='employee2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sale_order_employee2', to='brewsql.Employee', verbose_name='经办人'),
        ),
        migrations.AddField(
            model_name='saleorder',
            name='employee3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sale_order_employee3', to='brewsql.Employee', verbose_name='出库人'),
        ),
        migrations.AlterField(
            model_name='company',
            name='bank',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='开户行'),
        ),
        migrations.AlterField(
            model_name='company',
            name='bank_account',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='账户'),
        ),
        migrations.AlterField(
            model_name='saleorder',
            name='employee',
            field=models.ForeignKey(limit_choices_to={'is_salesman': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sale_order_employee', to='brewsql.Employee', verbose_name='销售员'),
        ),
        migrations.AlterField(
            model_name='saleorder',
            name='sale_order_code',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='订单编号'),
        ),
    ]
