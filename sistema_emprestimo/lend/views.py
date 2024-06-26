from django.shortcuts import render
from .models import Lend
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.models import User
from django.template import loader
from django.http import HttpResponse

class LendListView(ListView):
    model = Lend

class LendDetailView(DetailView):
    model = Lend

class LendCreateView(CreateView):
    model = Lend
    fields = ['id_account', 'id_book', 'lend_date', 'return_date']
    success_url = reverse_lazy('lend-list')

class LendUpdateView(UpdateView):
    model = Lend
    fields = ['id_account', 'id_book', 'lend_date', 'return_date']
    success_url = reverse_lazy('lend-list')

class LendDeleteView(DeleteView):
    model = Lend
    success_url = reverse_lazy('lend-list')

class LendNotificationView(ListView):
    model = Lend

    def get_queryset(self):
        return Lend.objects.filter(id_account=self.request.user.id)
