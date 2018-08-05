import logging
from django.shortcuts import render
from braces.views import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from . import forms
from . import models

sentry = logging.getLogger('sentry')

class ProfileView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = forms.ProfileForm
    template_name = "profile.html"

    def get_object(self, queryset=None):
        self.profile = models.Profile.objects.get(user=self.request.user)
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        return context
