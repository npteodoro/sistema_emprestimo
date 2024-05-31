from django.db import models
from django.contrib.auth.models import User
from library.models import Book

class Lend(models.Model):
    id_account = models.ForeignKey(User, on_delete=models.CASCADE)
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    lend_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.id_book} > {self.id_account}"
