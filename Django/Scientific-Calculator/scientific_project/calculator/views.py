from django.http import HttpResponse
from django.views.generic import FormView

from scientific_project.calculator.forms import SinusForm

from .sinus import sinus


class Home(FormView):

    template_name = 'base.html'
    form_class = SinusForm

    def form_valid(self, form):
        sin = sinus(float(form.cleaned_data.get('sinus')))
        return HttpResponse(sin)
