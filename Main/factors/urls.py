from django.conf.urls import include, url, patterns
from factors import views

urlpatterns = [
    url(r'home/', views.home, name='home'),
    url(r'analysis/', views.analysis, name='analysis'),
    url(r'userfilters/', views.getUserFilters, name='userfilters'),
    url(r'predict/', views.predict, name='predict')
]
