from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Mdata)
admin.site.register(models.Category)
admin.site.register(models.Subcategory)
admin.site.register(models.Brand)
admin.site.register(models.Type)
