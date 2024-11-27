from django.shortcuts import render
from django.views.generic import TemplateView

class ProfileView(TemplateView):
    template_name = 'profile.html'




class ReelsView(TemplateView):
    template_name = 'reels.html'

