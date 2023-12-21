import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from board.forms import AdForm, ResponseForm
from board.models import Ad


class AdsView(ListView):
    model = Ad
    ordering = '-created_at'
    template_name = 'ads_list.html'
    context_object_name = 'ads'
    # paginate_by = 10
    # search = False


class AdCreateView(LoginRequiredMixin, CreateView):
    raise_exception = True
    form_class = AdForm
    model = Ad
    template_name = 'ad_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.created_by = self.request.user

        return super(AdCreateView, self).form_valid(form)


class AdEditView(LoginRequiredMixin, UpdateView):
    raise_exception = True
    form_class = AdForm
    model = Ad
    template_name = 'ad_edit.html'


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ad_detail.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super(AdDetailView, self).get_context_data(**kwargs)
        context['response_form'] = ResponseForm()
        return context

    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:  # Проверка авторизации
            return HttpResponseForbidden("Доступ запрещен")

        logging.debug('post response')
        ad = self.get_object()
        form = ResponseForm(request.POST)
        if form.is_valid():
            resp = form.save(commit=False)
            resp.ad = ad
            resp.created_by = self.request.user
            resp.save()
        return self.get(request, *args, **kwargs)
