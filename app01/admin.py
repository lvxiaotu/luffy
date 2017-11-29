from django.contrib import admin
from app01 import models


# Register your models here.
admin.site.register(models.Course)
admin.site.register(models.PricePolicy)
admin.site.register(models.Coupon)
admin.site.register(models.CourseSubCategory)
admin.site.register(models.CourseCategory)
admin.site.register(models.Account)
admin.site.register(models.CouponRecord)
