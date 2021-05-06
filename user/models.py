from django.db import models


class User(models.Model):
    email            = models.EmailField(max_length=255, unique=True)
    name             = models.CharField(max_length=100)
    password         = models.CharField(max_length=200)
    corporation_name = models.CharField(max_length=200)
    phone_number     = models.CharField(max_length=30)
    is_verified      = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'

class GridLayout(models.Model):
    x            = models.IntegerField()
    y            = models.IntegerField()
    w            = models.IntegerField()
    h            = models.IntegerField()
    is_draggable = models.BooleanField(default=True)
    is_displyed  = models.BooleanField(default=True)
    grid_id      = models.CharField(max_length=100)
    user         = models.ForeignKey('User', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'grid_layouts'
        unique_together = ('user_id', 'grid_id')
