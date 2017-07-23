from django.http import HttpResponse
from django.views import generic
from braces import views
from . import models


class RestrictToUserMixin(object):
    def get_queryset(self):
        queryset = super(RestrictToUserMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class TalkListListView(views.LoginRequiredMixin, RestrictToUserMixin, generic.ListView):
    model = models.TalkList


class TalkListDetailView(views.LoginRequiredMixin, views.PrefetchRelatedMixin, RestrictToUserMixin, generic.DetailView):
    model = models.TalkList
    prefetch_related = ('talks', )
