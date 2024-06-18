from django.shortcuts import render
from .models import Book
from lend.models import Lend
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from barcode.writer import SVGWriter
from io import BytesIO
from barcode import EAN13

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

data = pd.DataFrame(list(Book.objects.all().values()))
# print(data.head())

# Convert 'average_rating' to a numeric data type
data['rating'] = pd.to_numeric(data['rating'], errors='coerce')

# Create a new column 'book_content' by combining 'title' and 'authors'
data['book_content'] = data['title'] + ' ' + data['author']

tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(data['book_content'])

# Compute the cosine similarity between books
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def recommend_books(book_title, cosine_sim=cosine_sim):
    # Get the index of the book that matches the title
    idx = data[data['title'] == book_title].index[0]

    # Get the cosine similarity scores for all books with this book
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the books based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top 5 most similar books (excluding the input book)
    sim_scores = sim_scores[1:6]

    # Get the book indices
    book_indices = [i[0] for i in sim_scores]

    # Return the top 10 recommended books
    return data['id'].iloc[book_indices]

class BookListView(ListView):
    model = Book
    #ordering = ['title']

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data()

        lent = Lend.objects.filter(id_account=self.request.user.id).order_by('-lend_date').first()

        if lent:
            book_title = lent.id_book.title
            context['recommended_list'] = Book.objects.filter(id__in=recommend_books(book_title).tolist())

        return context

class BookDetailView(DetailView):
    model = Book

@method_decorator(login_required, name='dispatch')
class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'cdd', 'local', 'rating']
    success_url = reverse_lazy('book-list')

@method_decorator(login_required, name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'cdd', 'local', 'rating']
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
