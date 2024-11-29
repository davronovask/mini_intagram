from django.shortcuts import render
from django.views.generic import TemplateView

class ProfileView(TemplateView):
    template_name = 'profile.html'

class HomeView(TemplateView):
    template_name = 'home.html'


class ReelsView(TemplateView):
    template_name = 'reels.html'

