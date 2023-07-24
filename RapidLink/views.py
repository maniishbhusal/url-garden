from django.shortcuts import render, redirect
from django.views import View
import pyshorteners
from django.urls import reverse
from .models import URLModel
import validators
# from .forms import URLModelForm


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'rapidlink/home.html', {
        })

    def post(self, request):
        entered_url = request.POST['url']

        # Validate the URL before saving it to the Database
        if not validators.url(entered_url):
            return redirect(reverse('url_error'))

        url_model = URLModel.objects.create(entered_url=entered_url)

        shortener = pyshorteners.Shortener()
        shorted_url = shortener.tinyurl.short(entered_url)
        url_model.short_url = shorted_url
        url_model.save()

        # Pass the short URL and entered URL as query parameters in the redirect URL
        redirect_url = reverse('shortener') + f'?short_url={shorted_url}&entered_url={entered_url}'
        return redirect(redirect_url)


class ShortenerView(View):
    def get(self, request):
        short_url = request.GET.get('short_url')
        entered_url = request.GET.get('entered_url')

        return render(request, 'rapidlink/shortener.html', {
            'short_url': short_url,
            'entered_url': entered_url,
        })

class URLErrorView(View):
    def get(self, request):
        return render(request, 'url_error.html', {
        })