from django.shortcuts import render


def index(request):
    template = "index/customers.html"
    return render(request, template)
