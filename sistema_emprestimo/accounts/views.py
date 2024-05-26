from django.shortcuts import render
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
