from django.db import models

# Create your models here.
class URLModel(models.Model):
    entered_url=models.URLField()
    short_url=models.CharField(max_length=20)

    def __str__(self):
        return self.entered_url
