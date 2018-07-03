from django.views.generic import FormView
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, ListAPIView

from .forms import MoodForm
from .models import Log
from .serializers import LogSerializer
from .mood_tracker import mood_tracker

import json
import datetime


class Home(FormView):

    template_name = 'home.html'
    form_class = MoodForm

    def form_valid(self, form):
        new_mood = mood_tracker(form.cleaned_data.get('mood_field'))

        log_entry = form.save(commit=False)
        log_entry.rating = new_mood
        log_entry.save()

        context = super().get_context_data()
        context.update({
            'result': new_mood,
            'moods': Log.objects.all()
        })

        #result_list = list(Log.objects.values('date', 'rating'))

        #with open('home/static/d3_data.json', 'w') as f:
        #    f.write(json.dumps(result_list, default=lambda x: x.strftime('%Y-%m-%d %H:%M:%S').__str__() if isinstance(x, datetime.datetime) else x))

        return super().render_to_response(context=context)


class LogListView(ListAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
