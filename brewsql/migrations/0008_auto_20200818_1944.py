# Generated by Django 2.2.13 on 2020-08-18 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brewsql', '0007_auto_20200818_1921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['-id'], 'verbose_name': '公司', 'verbose_name_plural': '公司'},
        ),
    ]