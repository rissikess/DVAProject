from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

# Create your views here.
def home(request):
    return render(request, "home/analysis.html", {})