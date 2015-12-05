from django.conf.urls import include, url, patterns
from reststats import views

urlpatterns = [
    url(r'home/', views.home, name='home'),
    url(r'reststats/', views.getRestStats, name='reststats')
]