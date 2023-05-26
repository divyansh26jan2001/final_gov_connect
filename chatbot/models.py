from django.db import models

# Create your models here.
class information(models.Model):
    SNo = models.AutoField(primary_key=True)
    que = models.CharField(max_length = 1000)
    ans = models.CharField(max_length=2000)

    
class electricity(models.Model):
    SNo = models.AutoField(primary_key=True)
    que = models.CharField(max_length = 1000)
    ans = models.CharField(max_length=2000)

class Jal_Jeevan_Mission(models.Model):
    SNo = models.AutoField(primary_key=True)
    que = models.CharField(max_length = 1000)
    ans = models.CharField(max_length=2000)

class raised_questions(models.Model):
    SNo = models.AutoField(primary_key=True)
    que = models.CharField(max_length= 1000)
    dept = models.CharField(max_length=100)