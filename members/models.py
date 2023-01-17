from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class Brand(models.Model):
    brand = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.brand

class Type(models.Model):
    type = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.type

class Category(models.Model):
    category = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.category


class Subcategory(models.Model):
    subname = models.CharField(max_length=200)
    subcategory = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.subname


class Mdata(models.Model):
    title = models.CharField(max_length = 200)
    subtitle = models.CharField(max_length = 200)
    price = models.IntegerField()
    detailes = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE,null=True)
    type = models.ForeignKey(Type,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE,null=True)
    rateing = models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(1)],null=True)
    file1 = models.FileField(null = True, blank = True)
    file2 = models.FileField(null = True, blank = True)
    file3 = models.FileField(null = True, blank = True)
    file4 = models.FileField(null = True, blank = True)
    file5 = models.FileField(null = True, blank = True)
    file6 = models.FileField(null = True, blank = True)

    def __str__(self):
        return self.title

    def Func(self):
        s, *d = str(self.price).partition(".")
        
        r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d)

    def rateingstar(self):
        a = []
        for i in range(1,self.rateing+1):
            a.append(i)
        a = a + [None] * (5 - len(a))
        # print(a)    
        return a    
    
           
