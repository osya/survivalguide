from django.views import generic
from braces import views
from . import models, forms


class RestrictToUserMixin(object):
    def get_queryset(self):
        queryset = super(RestrictToUserMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class TalkListListView(views.LoginRequiredMixin, RestrictToUserMixin, generic.ListView):
    model = models.TalkList


class TalkListDetailView(
        views.LoginRequiredMixin,
        views.PrefetchRelatedMixin,
        RestrictToUserMixin,
        generic.DetailView):
    model = models.TalkList
    prefetch_related = ('talks', )


class TalkListCreateView(views.LoginRequiredMixin, views.SetHeadlineMixin, generic.CreateView):
    form_class = forms.TalkListForm
    headline = 'Create'
    model = models.TalkList

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TalkListCreateView, self).form_valid(form)
