from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.conf import settings
import stripe

from .models import Product, ProductReview
from .forms import LocalProductForm, ProductReviewForm

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        search_query = request.GET.get('q')
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(category__type__icontains=search_query) |
                Q(category__categories__icontains=search_query) |
                Q(company__name__icontains=search_query)
            )
        return render(request, 'products/products_list.html', {'products': products})


class ProductDetailView(LoginRequiredMixin, View):
    def get_paginator_page(self, request, queryset):
        page_size = request.GET.get('page_size', 1)
        paginator = Paginator(queryset, page_size)
        page_num = request.GET.get('page', 1)
        return paginator.get_page(page_num)

    def get(self, request, id):
        product = Product.objects.get(id=id)
        pictures = product.productpicture_set.all()
        page_obj = self.get_paginator_page(request, pictures)
        review_form = ProductReviewForm()
        return render(request, 'products/products_detail.html',
                      {'product': product, 'page_obj': page_obj, 'review_form': review_form})

    def post(self, request, id):
        product = Product.objects.get(id=id)
        review_form = ProductReviewForm(data=request.POST)
        pictures = product.productpicture_set.all()
        page_obj = self.get_paginator_page(request, pictures)

        if review_form.is_valid():
            ProductReview.objects.create(
                product=product,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )
            return redirect(reverse('products:product_detail', kwargs={'id': product.id}))

        messages.error(request, 'Please correct your review form.')
        return render(request, 'products/products_detail.html',
                      {'product': product, 'page_obj': page_obj, 'review_form': review_form})


class CheckoutView(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        return render(request, 'products/payment.html', {'product': product})


class ProductPaymentView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = request.build_absolute_uri('/')[:-1]  # dynamic domain

        # Create a Price object for Stripe
        price = stripe.Price.create(
            unit_amount=int(product.price * 100),
            currency='usd',
            product_data={'name': product.name},
        )

        checkout_session = stripe.checkout.Session.create(
            line_items=[{'price': price.id, 'quantity': 1}],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )

        return HttpResponseRedirect(checkout_session.url)


class SellProductListView(LoginRequiredMixin, View):
    def get(self, request):
        form = LocalProductForm()
        products = Product.objects.all()
        return render(request, 'products/sell_product.html', {'form': form, 'products': products})

    def post(self, request):
        form = LocalProductForm(data=request.POST, files=request.FILES)
        form.files_data = request.FILES  # <-- crucial for multiple images
        if form.is_valid():
            form.set_user(request.user)
            form.save()
            messages.success(request, 'Your product has been added for sale.')
            return redirect('products:product_sell')

        return render(request, 'products/sell_product.html', {'form': form})
    
class DeleteProductView(LoginRequiredMixin, View):
    def post(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            messages.error(request, "Product does not exist.")
            return redirect('products:product_sell')

        # Only allow the owner to delete
        if product.user != request.user:
            return HttpResponseForbidden("You cannot delete this product.")

        product.delete()
        messages.success(request, "Your product has been deleted.")
        return redirect('products:product_sell')
    


class DeleteProductReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        try:
            review = ProductReview.objects.get(id=id)
        except ProductReview.DoesNotExist:
            messages.error(request, "Review does not exist.")
            return redirect('products:product_sell')  # fallback redirect

        # Only the owner can delete
        if review.user != request.user:
            return HttpResponseForbidden("You cannot delete this review.")

        review.delete()
        messages.success(request, "Your review has been deleted.")
        # Redirect back to the product detail page
        return redirect('products:product_detail', id=review.product.id)
    
class EditProductReviewView(LoginRequiredMixin, View):
    def get(self, request, id):
        try:
            review = ProductReview.objects.get(id=id)
        except ProductReview.DoesNotExist:
            messages.error(request, "Review does not exist.")
            return redirect('products:product_list')

        if review.user != request.user:
            return HttpResponseForbidden("You cannot edit this review.")

        form = ProductReviewForm(instance=review)
        return render(request, 'products/edit_review.html', {'form': form, 'review': review})

    def post(self, request, id):
        try:
            review = ProductReview.objects.get(id=id)
        except ProductReview.DoesNotExist:
            messages.error(request, "Review does not exist.")
            return redirect('products:product_list')

        if review.user != request.user:
            return HttpResponseForbidden("You cannot edit this review.")

        form = ProductReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Your review has been updated.")
            return redirect('products:product_detail', id=review.product.id)
        else:
            messages.error(request, "Please fix the errors below.")
            return render(request, 'products/edit_review.html', {'form': form, 'review': review})
