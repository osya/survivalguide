from django.views import generic
from braces import views
from . import models, forms


class RestrictToUserMixin(object):
    def get_queryset(self):
        queryset = super(RestrictToUserMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class TalkListListView(RestrictToUserMixin, views.LoginRequiredMixin, generic.ListView):
    model = models.TalkList


class TalkListDetailView(
        RestrictToUserMixin,
        views.LoginRequiredMixin,
        views.PrefetchRelatedMixin,
        generic.DetailView):
    model = models.TalkList
    prefetch_related = ('talks', )

    def get_object(self):
        talk_list = super(TalkListDetailView, self).get_object()
        return forms.TalkListDetailForm(instance=talk_list)


class TalkListCreateView(views.LoginRequiredMixin, views.SetHeadlineMixin, generic.CreateView):
    form_class = forms.TalkListForm
    headline = 'Create List'
    model = models.TalkList

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TalkListCreateView, self).form_valid(form)


class TalkListUpdateView(RestrictToUserMixin, views.LoginRequiredMixin, views.SetHeadlineMixin, generic.UpdateView):
    form_class = forms.TalkListForm
    headline = 'Update List'
    model = models.TalkList
