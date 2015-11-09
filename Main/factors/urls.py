from django.conf.urls import include, url, patterns
from factors import views

urlpatterns = [
    url(r'home/', views.home, name='home'),
]
