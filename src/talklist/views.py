from braces.views import FormValidMessageMixin, PrefetchRelatedMixin, SetHeadlineMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
# Create your views here.
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from rest_framework import permissions, viewsets

from permissions import IsOwnerOrReadOnly
from talk.forms import TalkForm
from talk.models import Talk
from talklist.forms import TalkListForm
from talklist.models import TalkList
from talklist.serializers import TalkListSerializer


class RestrictToUserMixin(View):
    def get_queryset(self):
        assert isinstance(self, (SingleObjectMixin, MultipleObjectMixin))
        queryset = super(RestrictToUserMixin, self).get_queryset()
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class TalkListListView(ListView):
    model = TalkList
    queryset = TalkList.objects.list()


# class TalkListDetailView(
#         LoginRequiredMixin,
#         RestrictToUserMixin,
#         PrefetchRelatedMixin,
#         DetailView,
#         CreateView):
#     """
#         TalkListDetailView variant based on CreateView
#     """
#     http_method_names = ['get', 'post']
#     model = TalkList
#     prefetch_related = ('talks',)
#     template_name = 'talks/talklist_detail.html'
#     form_class = TalkForm
#
#     def get_context_data(self, **kwargs):
#         # super(TalkListDetailView, self).get_context_data(**kwargs) don't use here.
#         # Because due to MRO called FormMixin.get_context_data()
#         context = DetailView.get_context_data(self, **kwargs)
#         context['form'] = self.form_class(self.request.POST or {'talklist': kwargs['object']})
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
#             kwargs.pop('instance', None)
#         return kwargs
#
#     def form_valid(self, form):
#         """
#         If the form is valid, save the associated model.
#         """
#         # used FormView.form_valid(self, form) here.
#         # Because ModelFormMixin.form_valid() makes self.object = form.save()
#         form.save()
#         return FormView.form_valid(self, form)


class TalkListDetailView(LoginRequiredMixin, RestrictToUserMixin, PrefetchRelatedMixin, DetailView):
    """
        TalkListDetailView variant without CreateView inheritance
    """
    form_class = TalkForm
    http_method_names = ['get', 'post']
    model = TalkList
    prefetch_related = ('talks', )

    def get_context_data(self, **kwargs):
        context = super(TalkListDetailView, self).get_context_data(**kwargs)
        context.update({'form': self.form_class(self.request.POST or {'talklist': kwargs['object']})})
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
        else:
            return self.get(request, *args, **kwargs)
        return redirect(form.instance.talklist)


class TalkListCreateView(LoginRequiredMixin, SetHeadlineMixin, CreateView):
    form_class = TalkListForm
    headline = 'Create List'
    model = TalkList
    object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(TalkListCreateView, self).form_valid(form)


class TalkListUpdateView(LoginRequiredMixin, RestrictToUserMixin, SetHeadlineMixin, UpdateView):
    form_class = TalkListForm
    headline = 'Update List'
    model = TalkList


class TalkListDeleteTalkView(LoginRequiredMixin, FormValidMessageMixin, DeleteView):
    model = Talk

    def get_success_url(self):
        return self.object.talklist.get_absolute_url()

    def get_form_valid_message(self):
        return '{0.name} was removed from {1.name}'.format(self.object, self.object.talklist)


class TalkListScheduleView(RestrictToUserMixin, PrefetchRelatedMixin, DetailView):
    model = TalkList
    prefetch_related = ('talks', )
    template_name = 'talklist/schedule.html'


class TalkListViewSet(viewsets.ModelViewSet):
    serializer_class = TalkListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = TalkList.objects.list()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
