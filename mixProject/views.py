from django.shortcuts import render
from products.models import CompanyNews


def landing_page(request):
    news = CompanyNews.objects.all()
    return render(request, 'landing.html', {'news': news})




