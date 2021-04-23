from django.db import models


class ChargePoint(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)


class AccessRight(models.Model):
    charge_point = models.ForeignKey(to='ChargePoint', on_delete=models.CASCADE)
    #id = models.CharField(max_length=16)


#class User_Account(models.Model):
#    Access_Right = models.ForeignKey(to='Access_Right', on_delete=models.RESTRICT)

