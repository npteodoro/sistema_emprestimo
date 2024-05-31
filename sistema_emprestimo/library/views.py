from django.shortcuts import render
from .models import Book
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from barcode.writer import SVGWriter
from io import BytesIO
from barcode import EAN13

class BookListView(ListView):
    model = Book

class BookDetailView(DetailView):
    model = Book

@method_decorator(login_required, name='dispatch')
class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'cdd', 'local']
    success_url = reverse_lazy('book-list')

@method_decorator(login_required, name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'cdd', 'local']
    success_url = reverse_lazy('book-list')

@method_decorator(login_required, name='dispatch')
class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('book-list')

def barcode(request, id):
    rv = BytesIO()
    EAN13(str(id).zfill(12), writer=SVGWriter()).write(rv)
    image = rv.getvalue().decode()
    return HttpResponse(image, content_type="image/svg+xml")
