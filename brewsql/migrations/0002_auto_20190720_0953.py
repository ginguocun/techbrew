# Generated by Django 2.2 on 2019-07-20 01:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brewsql', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pack',
            options={'ordering': ['-pk'], 'permissions': (('can_export_pack_data', '可以导出入库记录'),), 'verbose_name': '产品入库', 'verbose_name_plural': '产品入库'},
        ),
        migrations.AddField(
            model_name='moneyinout',
            name='appendix',
            field=models.FileField(blank=True, null=True, upload_to='money_in_out', verbose_name='附件'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='pack',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='brewsql.Pack', verbose_name='灌装批次'),
        ),
    ]
