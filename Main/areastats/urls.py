from django.conf.urls import include, url, patterns
from areastats import views

urlpatterns = [
    url(r'home/', views.home, name='home'),
    url(r'stats/', views.getStats, name='stats')
]