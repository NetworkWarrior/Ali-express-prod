from django.contrib import admin
from .models import Category, Company, Product, ProductReview, ProductPicture, CompanyNews
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    search_fields = 'type'


class CompanyAdmin(admin.ModelAdmin):
    search_fields = 'name'


class ReviewAdmin(admin.ModelAdmin):
    search_fields = ('product', 'comment')


class ProductAdmin(admin.ModelAdmin):
    search_fields = 'name'


class CompanyNewsAdmin(admin.ModelAdmin):
    search_fields = 'name'



admin.site.register(Company)
admin.site.register(Product)
admin.site.register(ProductReview)
admin.site.register(Category)
admin.site.register(ProductPicture)
admin.site.register(CompanyNews)
