from datetime import datetime
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from accounts.models import CustomUser
# Create your models here.


class Category(models.Model):
    type = models.CharField(max_length=100, blank=True)
    categories = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.type}, {self.categories}"


class Company(models.Model):
    name = models.CharField(max_length=30)
    icon = models.ImageField(default='default_company_pic.jpg')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, default='none')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    europe_delivery = models.IntegerField(default=7, blank=True)
    europe_out_delivery = models.IntegerField(default=12, blank=True)
    sold_count = models.IntegerField(default=0, blank=True)
    local = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def set_user(self, user):
        self.user = user

    def average_rating(self):
        reviews = self.productreview_set.all()
        if reviews.count() > 0:
            total_stars = sum(review.stars_given for review in reviews)
            average_stars = total_stars / reviews.count()
            return format(average_stars, '.1f')
        else:
            return 0.0

    def __str__(self):
        return self.name

    def get_int_decimal(self):
        price_decimal = Decimal(str(self.price))
        price_integer = int(price_decimal)
        return price_integer

    def delivery_price(self):
        price_decimal = Decimal(str(self.price))
        delivery_price = price_decimal / 10
        return "{:.2f}".format(delivery_price)

    def get_decimal_price(self):
        price_decimal = Decimal(str(self.price))
        price_decimal_part = (price_decimal % 1) * 100  # multiply by 100 to get the integer part
        decimal_integer = int(price_decimal_part)
        return decimal_integer

    def sell(self):
        self.sold_count += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.email and self.user:
            self.email = self.user.email
        super(Product, self).save(*args, **kwargs)


    def get_first_picture(self):
        first_picture = self.productpicture_set.order_by('id').first()
        if first_picture:
            return first_picture.picture.url
        return None

    def get_next_picture(self, current_picture):
        next_picture = self.productpicture_set.filter(order__gt=current_picture.order).order_by('order').first()
        if next_picture:
            return next_picture.picture.url
        else:
            return None

    def get_first_picture(self):
        try:
            return self.productpicture_set.first().picture.url
        except AttributeError:
            return None

class ProductPicture(models.Model):
    picture = models.ImageField(default='product_image.png')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.IntegerField(default=0)

    def get_image(self):
        return self.picture

    def __str__(self):
        return self.product.name



class ProductReview(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stars_given = models.FloatField(
        default=0, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'by {self.user} for {self.product.name}'


class CompanyNews(models.Model):
    name = models.CharField(blank=True, max_length=150)
    description = models.TextField(max_length=400)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True)
    deleted_in = models.IntegerField(default=7, blank=True)
    discount = models.IntegerField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def days_since_created(self):
        now = datetime.now(timezone.utc)
        delta = now - self.created_at
        return delta.days

    def discount_price(self):
        if self.should_displayed:
            if self.discount:
                price = self.product.price - ((self.product.price * self.discount)/100)
                price = "{:.2f}".format(price)
                return price

    def should_be_deleted(self):
        if self.days_since_created() < self.deleted_in:
            days = self.deleted_in - self.days_since_created()
            if days > 1:
                ready = f"{days} days to be expired"
            else:
                ready = f"last-day to be expired"
            return ready

    def should_displayed(self):
        if self.days_since_created() > self.deleted_in:
            return False
        else:
            return True

    def __str__(self):
        return f"news for {self.product.name} by {self.company}"



