import random
import string
from django.shortcuts import render, redirect
from django.views import View
import pyshorteners
from django.urls import reverse
from .models import URLModel
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.views.generic.base import TemplateView



# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'rapidlink/home.html', {})

    def post(self, request):
        entered_url = request.POST['url']

        # Validate the URL before saving it to the Database
        url_validator = URLValidator()
        try:
            url_validator(entered_url)
        except ValidationError:
            messages.error(request, 'Invalid URL')
            return redirect('home')

        # Check if the entered URL already exists in the database
        if URLModel.objects.filter(entered_url=entered_url).exists():
            url_model = URLModel.objects.get(entered_url=entered_url)
        else:
            # Generate a unique short URL
            shorted_url = self.generate_short_url()

            # Create a new URLModel instance
            url_model = URLModel.objects.create(entered_url=entered_url, short_url=shorted_url)

         # Store the short URL and entered URL in the session
        request.session['short_url'] = url_model.short_url
        request.session['entered_url'] = entered_url

        # Redirect to the ShortenerView
        return redirect(reverse('shortener'))

    def generate_short_url(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(8))


class ShortenerView(View):
    def get(self, request):
          # Retrieve the short URL and entered URL from the session
        short_url = request.session.get('short_url')
        entered_url = request.session.get('entered_url')

        if not short_url or not entered_url:
            messages.error(request,"Please submit a URL first.")
            return redirect(reverse('home'))

        
        # Optionally, you can also remove the session data here to prevent future access
        del request.session['short_url']
        del request.session['entered_url']

        return render(request, 'rapidlink/shortener.html', {
            'short_url': short_url,
            'entered_url': entered_url,
        })

class URLErrorView(TemplateView):
    template_name = 'url_error.html'

