from django.http import HttpResponse
from django.views import generic


class TalkListDetailView(generic.View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('a talk list')
