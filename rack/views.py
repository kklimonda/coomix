from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.generic.edit import UpdateView

from core.models import User
from rack.forms import UpdateSubscriptionsForm
from rack.models import Comic


class UpdateSubscriptionsView(UpdateView):
    model = User
    form_class = UpdateSubscriptionsForm
    fields = ('subscriptions',)
    template_name = 'rack/manage.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user
