from django.http import HttpResponse
from django.views import generic
from braces import views
from . import models


class TalkListListView(views.LoginRequiredMixin, generic.ListView):
    model = models.TalkList

    def get_queryset(self):
        return self.request.user.lists.all()


class TalkListDetailView(generic.View):
    @staticmethod
    def get(request, *args, **kwargs):
        return HttpResponse('a talk list')
