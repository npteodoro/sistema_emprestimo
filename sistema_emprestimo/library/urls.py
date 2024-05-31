from django.urls import include, path
from . import views
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView

urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path("<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("add/", BookCreateView.as_view(), name="book-add"),
    path("<int:pk>/edit/", BookUpdateView.as_view(), name="book-update"),
    path("<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
]
