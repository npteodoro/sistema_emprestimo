from django.shortcuts import render
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from barcode import EAN13
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from barcode.writer import SVGWriter

class SignUpView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def profile(request):
    myuser = User.objects.get(username=request.user)
    template = loader.get_template('profile.html')
    context = {
    'myuser': myuser,
  }
    return HttpResponse(template.render(context, request))

@login_required
def barcode(request):
    myuser = User.objects.get(username=request.user)
    image=EAN13(str(myuser.id).zfill(13), writer=SVGWriter())
    return HttpResponse(image, content_type="image/svg+xml")