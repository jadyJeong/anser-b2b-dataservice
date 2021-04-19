# Generated by Django 3.2 on 2021-04-19 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_corporation_jurir_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ceoname',
            name='corporation',
        ),
        migrations.RemoveField(
            model_name='corporationclassification',
            name='corporation',
        ),
        migrations.RemoveField(
            model_name='currencyunit',
            name='income_statement',
        ),
        migrations.RemoveField(
            model_name='incomestatement',
            name='corporation',
        ),
        migrations.RemoveField(
            model_name='industrycode',
            name='corporation',
        ),
        migrations.RemoveField(
            model_name='mainshareholder',
            name='corporation',
        ),
        migrations.RemoveField(
            model_name='stocktype',
            name='main_shareholder',
        ),
        migrations.DeleteModel(
            name='AccountingMonth',
        ),
        migrations.DeleteModel(
            name='CeoName',
        ),
        migrations.DeleteModel(
            name='Corporation',
        ),
        migrations.DeleteModel(
            name='CorporationClassification',
        ),
        migrations.DeleteModel(
            name='CurrencyUnit',
        ),
        migrations.DeleteModel(
            name='IncomeStatement',
        ),
        migrations.DeleteModel(
            name='IndustryCode',
        ),
        migrations.DeleteModel(
            name='MainShareholder',
        ),
        migrations.DeleteModel(
            name='StockType',
        ),
    ]
