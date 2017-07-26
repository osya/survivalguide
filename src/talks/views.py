from django.contrib import messages
from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect
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

    def get_queryset(self):
        queryset = super(TalkListListView, self).get_queryset()
        queryset = queryset.annotate(talk_count=Count('talks'))
        return queryset


class TalkListDetailView(
        RestrictToUserMixin,
        views.LoginRequiredMixin,
        views.PrefetchRelatedMixin,
        generic.DetailView):
    form_class = forms.TalkForm
    http_method_names = ['get', 'post']
    model = models.TalkList
    prefetch_related = ('talks', )

    def get_context_data(self, **kwargs):
        context = super(TalkListDetailView, self).get_context_data(**kwargs)
        context.update({'form': self.form_class(self.request.POST or None)})
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            talk_list = self.get_object()
            talk = form.save(commit=False)
            talk.talk_list = talk_list
            talk.save()
        else:
            return self.get(request, *args, **kwargs)
        return redirect(talk_list)


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


class TalkListDeleteTalkView(views.LoginRequiredMixin, generic.RedirectView):
    model = models.Talk

    def get_redirect_url(self, *args, **kwargs):
        return self.talk_list.get_absolute_url()

    def get_object(self, pk, talk_list_pk):
        try:
            talk = self.model.objects.get(pk=pk, talk_list_id=talk_list_pk, talk_list__user=self.request.user)
        except models.Talk.DoesNotExist:
            raise Http404
        else:
            return talk

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(kwargs.get('pk'), kwargs.get('talk_list_pk'))
        self.talk_list = self.object.talk_list
        messages.success(request, '{0.name} was removed from {1.name}'.format(self.object, self.talklist))
        self.object.delete()
        return super(TalkListDeleteTalkView, self).get(request, *args, **kwargs)


class TalkListScheduleView(
        RestrictToUserMixin,
        views.PrefetchRelatedMixin,
        generic.DetailView
):
    model = models.TalkList
    prefetch_related = ('talks',)
    template_name = 'talks/schedule.html'
