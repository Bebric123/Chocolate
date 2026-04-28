# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import math


class MaterialProducts(models.Model):
    qty_material_product = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    material = models.ForeignKey('Materials', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Products', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Material_products'


class MaterialSuppliers(models.Model):
    zak_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    avg_delivery = models.IntegerField(blank=True, null=True)
    material = models.ForeignKey('Materials', models.DO_NOTHING, blank=True, null=True)
    supplier = models.ForeignKey('Suppliers', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Material_suppliers'


class MaterialType(models.Model):
    type_material = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    percent_lost = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Material_type'

    def __str__(self):
        return self.type_material


class Materials(models.Model):
    name_material = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    price_unit = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    qty_werehouse = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    min_qty = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    qty_pack = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    type = models.ForeignKey(MaterialType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Materials'

    def stock_value(self):
        if self.qty_werehouse < self.min_qty:
            qty = self.min_qty - self.qty_werehouse
            summ = math.ceil((qty/self.qty_pack) * self.price_unit)
            return summ
        else:
            return 0.00


class ProductType(models.Model):
    type_product = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    coeff_product = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Product_type'


class Products(models.Model):
    arcticle = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    name_product = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    min_price = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    type = models.ForeignKey(ProductType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Products'


class Roles(models.Model):
    name_role = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    desc_perm = models.CharField(max_length=100, db_collation='Cyrillic_General_CI_AS')

    class Meta:
        managed = False
        db_table = 'Roles'


class Suppliers(models.Model):
    type_supplier = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    name_supplier = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    inn = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    rating = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Suppliers'


class Users(models.Model):
    login = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    full_name = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    email = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    active = models.CharField(max_length=50, db_collation='Cyrillic_General_CI_AS')
    role = models.ForeignKey(Roles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='Cyrillic_General_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
