from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cdd = models.CharField(max_length=255)
    local = models.CharField(max_length=255)
    rating = models.FloatField(null = True)

    def __str__(self):
        return f"{self.title}"
