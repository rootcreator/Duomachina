from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class ContactView(TemplateView):
    template_name = 'pages/contact.html'

class TermsView(TemplateView):
    template_name = 'pages/terms.html'

class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'
