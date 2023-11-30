from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import CreationForm


class SingUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('payment:index')
    template_name = 'users/signup.html'
