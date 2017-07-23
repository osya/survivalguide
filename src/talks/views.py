from django.http import HttpResponse
from django.views import generic
from braces import views
from . import models


class TalkListListView(views.LoginRequiredMixin, generic.ListView):
    model = models.TalkList

    def get_queryset(self):
        return self.request.user.lists.all()


class TalkListDetailView(views.LoginRequiredMixin, views.PrefetchRelatedMixin, generic.DetailView):
    model = models.TalkList
    prefetch_related = ('talks', )

    def get_queryset(self):
        queryset = super(TalkListDetailView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset
