from django.db import models


class Corporation(models.Model):
    id                         = models.CharField(max_length=50, primary_key=True)
    cocode                     = models.CharField(max_length=8)
    coname                     = models.CharField(max_length=200)
    coname_eng                 = models.CharField(max_length=200, null=True)
    stock_name                 = models.CharField(max_length=200, null=True)
    jurir_no                   = models.CharField(max_length=50, unique=True, null=True)
    bizr_no                    = models.CharField(max_length=50, unique=True, null=True)
    adres                      = models.CharField(max_length=200, null=True)
    hm_url                     = models.CharField(max_length=500, null=True)
    ir_url                     = models.CharField(max_length=500, null=True)
    phn_no                     = models.CharField(max_length=50, null=True)
    fax_no                     = models.CharField(max_length=50, null=True)
    est_dt                     = models.DateField(null=True)
    is_financial_corporation   = models.BooleanField()
    accounting_month           = models.ForeignKey('AccountingMonth', on_delete=models.RESTRICT)
    corporation_classification = models.ForeignKey('CorporationClassification', on_delete=models.RESTRICT)
    industry_code              = models.ForeignKey('IndustryCode', on_delete=models.RESTRICT)
    conglomerate               = models.ManyToManyField('Conglomerate', through='ConglomerateCorporation')

    class Meta:
        db_table = 'corporations'


class CeoName(models.Model):
    name        = models.CharField(max_length=100)
    corporation = models.ForeignKey('Corporation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'ceo_names'


class CorporationClassification(models.Model):
    symbol             = models.CharField(max_length=1)
    symbol_description = models.CharField(max_length=20)

    class Meta:
        db_table = 'corporation_classifications'


class AccountingMonth(models.Model):
    month = models.IntegerField()

    class Meta:
        db_table = 'accounting_months'


class IndustryCode(models.Model):
    code = models.CharField(max_length=50)

    class Meta:
        db_table = 'industry_codes'


class MainShareholder(models.Model):
    rcept_no                  = models.CharField(max_length=20)
    nm                        = models.CharField(max_length=50)
    bsis_posesn_stock_co      = models.DecimalField(max_digits=20, decimal_places=2)
    bsis_posesn_stock_qota_rt = models.DecimalField(max_digits=20, decimal_places=2)
    corporation               = models.ForeignKey('Corporation', on_delete=models.CASCADE)
    stock_type                = models.ForeignKey('StockType', on_delete=models.RESTRICT)

    class Meta:
        db_table = 'main_shareholders'


class StockType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'stock_types'


class IncomeStatement(models.Model):
    year_month     = models.DateField(null=True)
    sales_ind      = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    ebit_ind       = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    ni_ind         = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    sales_con      = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    ebit_con       = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    ni_con         = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    ni_control_con = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    asset_ind      = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    asset_con      = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    corporation    = models.ForeignKey('Corporation', on_delete=models.CASCADE)
    currency_unit  = models.ForeignKey('CurrencyUnit', on_delete=models.RESTRICT)

    class Meta:
        db_table = 'income_statements'


class CurrencyUnit(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'currency_units'


class ConglomerateCorporation(models.Model):
    conglomerate = models.ForeignKey('Conglomerate', on_delete=models.CASCADE)
    corporation  = models.ForeignKey('Corporation', on_delete=models.CASCADE)

    class Meta:
        db_table = 'conglomerates_corporations'


class Conglomerate(models.Model):
    designate         = models.DateField(null=True)
    conglomerate      = models.CharField(max_length=50, null=True)
    tycoon            = models.CharField(max_length=50, null=True)
    nfirms            = models.IntegerField(null=True)
    nfirms_public     = models.IntegerField(null=True)
    at_regular        = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    teq               = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    sale              = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    ni                = models.DecimalField(max_digits=20,decimal_places=2, null=True)
    gcode             = models.CharField(max_length=50, unique=True)
    currency_unit     = models.ForeignKey('CurrencyUnit', on_delete=models.RESTRICT)
    conglomerate_type = models.ForeignKey('ConglomerateType', on_delete=models.RESTRICT)

    class Meta:
        db_table = 'conglomerates'


class ConglomerateType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'conglomerate_types'
