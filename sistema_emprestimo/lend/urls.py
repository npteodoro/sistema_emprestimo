from django.urls import path
from .views import LendListView, LendDetailView, LendCreateView, LendUpdateView, LendDeleteView

urlpatterns = [
    path('', LendListView.as_view(), name='lend-list'),
    path("<int:pk>/", LendDetailView.as_view(), name="lend-detail"),
    path("add/", LendCreateView.as_view(), name="lend-add"),
    path("<int:pk>/edit/", LendUpdateView.as_view(), name="lend-update"),
    path("<int:pk>/delete/", LendDeleteView.as_view(), name="lend-delete"),
]
