from braces import views
from django.db.models import Count
from django.shortcuts import redirect
from django.views import generic
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin

from . import models, forms


class RestrictToUserMixin(View):
    def get_queryset(self):
        assert isinstance(self, (SingleObjectMixin, MultipleObjectMixin))
        assert isinstance(self, View)
        queryset = super(RestrictToUserMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class TalkListListView(RestrictToUserMixin, views.LoginRequiredMixin, generic.ListView):
    model = models.TalkList

    def get_queryset(self):
        queryset = super(TalkListListView, self).get_queryset()
        queryset = queryset.annotate(talk_count=Count('talks'))
        return queryset


# class TalkListDetailView(
#         RestrictToUserMixin,
#         views.LoginRequiredMixin,
#         views.PrefetchRelatedMixin,
#         generic.DetailView,
#         generic.CreateView):
#     """
#         TalkListDetailView variant based on CreateView
#     """
#     http_method_names = ['get', 'post']
#     model = models.TalkList
#     prefetch_related = ('talks',)
#     template_name = 'talks/talklist_detail.html'
#     form_class = forms.TalkForm
#
#     def get_context_data(self, **kwargs):
#         # super(TalkListDetailView, self).get_context_data(**kwargs) don't use here.
#         # Because due to MRO called FormMixin.get_context_data()
#         context = generic.DetailView.get_context_data(self, **kwargs)
#         context['form'] = self.form_class(self.request.POST or {'talk_list': kwargs['object']})
#         return context
#
#     def post(self, *args, **kwargs):
#         # BaseCreateView.post() makes self.object = None, and ProcessFormView.post() is not accessible
#         # In POST request self.object (TalkList) is needed for redirect
#         self.object = self.get_object()
#         form = self.get_form()
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def get_form(self):
#         return self.form_class(**self.get_form_kwargs())
#
#     def get_form_kwargs(self):
#         """
#         Returns the keyword arguments for instantiating the form.
#         """
#         kwargs = super(TalkListDetailView, self).get_form_kwargs()
#         # 'object' key is a TalkList object. But this form requires Talk object. So popped it
#         if 'instance' in kwargs:
#             kwargs.pop('instance')
#         return kwargs
#
#     def form_valid(self, form):
#         """
#         If the form is valid, save the associated model.
#         """
#         # used generic.FormView.form_valid(self, form) here.
#         # Because ModelFormMixin.form_valid() makes self.object = form.save()
#         form.save()
#         return generic.FormView.form_valid(self, form)


class TalkListDetailView(
        RestrictToUserMixin,
        views.LoginRequiredMixin,
        views.PrefetchRelatedMixin,
        generic.DetailView):
    """
        TalkListDetailView variant without CreateView inheritance
    """
    form_class = forms.TalkForm
    http_method_names = ['get', 'post']
    model = models.TalkList
    prefetch_related = ('talks',)

    def get_context_data(self, **kwargs):
        context = super(TalkListDetailView, self).get_context_data(**kwargs)
        context.update({'form': self.form_class(self.request.POST or {'talk_list': kwargs['object']})})
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        else:
            return self.get(request, *args, **kwargs)
        return redirect(form.instance.talk_list)


class TalkListCreateView(views.LoginRequiredMixin, views.SetHeadlineMixin, generic.CreateView):
    form_class = forms.TalkListForm
    headline = 'Create List'
    model = models.TalkList
    object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TalkListCreateView, self).form_valid(form)


class TalkListUpdateView(RestrictToUserMixin, views.LoginRequiredMixin, views.SetHeadlineMixin, generic.UpdateView):
    form_class = forms.TalkListForm
    headline = 'Update List'
    model = models.TalkList


class TalkListDeleteTalkView(views.LoginRequiredMixin, views.FormValidMessageMixin, generic.DeleteView):
    model = models.Talk

    def get_success_url(self, *args, **kwargs):
        return self.object.talk_list.get_absolute_url()

    def get_form_valid_message(self):
        return '{0.name} was removed from {1.name}'.format(self.object, self.object.talk_list)


class TalkListScheduleView(
        RestrictToUserMixin,
        views.PrefetchRelatedMixin,
        generic.DetailView
):
    model = models.TalkList
    prefetch_related = ('talks',)
    template_name = 'talks/schedule.html'

# TODO: Create REST API
# TODO: Этот проект Survival Guide интегрировать в проект Todolist и после этого проект Survival Guide удалить из Heroku
