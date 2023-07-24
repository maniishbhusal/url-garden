from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('shortener/',views.ShortenerView.as_view(), name='shortener'),
    path('url_error/',views.URLErrorView.as_view(), name='url_error'),
    path('<str:short_url>/',views.RedirectView.as_view(), name='redirect'),
]