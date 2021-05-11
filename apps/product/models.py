from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Employee(models.Model):
    DESIGNATION = (
          ("Team Lead", "Team Lead"),
          ("Sr. Developer", "Sr. Developer"),
          ("Jr. Developer", "Jr. Developer"),
    )
    name = models.CharField(max_length=100)
    designation = models.CharField(choices=DESIGNATION,max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    


class Item(models.Model):
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ItemAssign(models.Model):
    assign_to = models.ForeignKey('Employee',on_delete=models.CASCADE)
    assign_item = models.ForeignKey('Item',on_delete= models.CASCADE)
    assign_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.assign_to.name

class SellItems(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.name