from django.shortcuts import render

from django.views.generic import TemplateView
# Create your views here.


class HomeView(TemplateView):
    """Very first template to see."""

    template_name = 'a01/home.html'
