import logging

from allauth.account.models import EmailAddress
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, ListView

from board.models import Response, Ad
from .filters import AdFilter
from .forms import ConfirmEmailForm
from .models import EmailVerify


class ConfirmEmail(TemplateView):
    template_name = 'account/verification_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ConfirmEmailForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ConfirmEmailForm(request.POST)  # Создание объекта формы с данными из POST-запроса

        if not form.is_valid():
            return self.get(request, *args, **kwargs)

        key = form.cleaned_data['confirmation_code']

        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        logging.debug(f'key: {key}')
        logging.debug(f'User: {user}')

        valid_key = EmailVerify.objects.filter(user=user, key=key).exists()
        if not valid_key:
            form.errors.clear()
            form.add_error('confirmation_code', 'Неверный код подтверждения')
            return render(request, self.template_name, {'form': form})

        EmailAddress.objects.get(user=user).set_verified()
        # Если все проверки прошли, авторизую пользователя и отправляю на доску
        login(request, user)
        return HttpResponseRedirect(reverse("home"))


class UserProfile(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'account/user_profile.html'
    context_object_name = 'user_ads'

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(created_by=user)
        self.filterset = AdFilter(self.request.GET, queryset)

        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_responses = Response.objects.filter(created_by=user)
        context['user_responses'] = user_responses

        context['filterset'] = self.filterset

        return context


@login_required
@csrf_protect
def accept_response(request, pk):
    logging.debug('accept response')
    response = Response.objects.get(id=pk)

    if response.ad.created_by != request.user:
        # Ответить на отклик может только автор объявления, даже если он сам оставил отклик
        return redirect('user_profile', request.user.username)

    response.accept = True
    response.save()

    # text_response = response.text
    # email = response.created_by.email
    # ad = response.ad
    # ad_title = ad.title
    #
    # subject = f'Ваш отклик принят'
    # text_content = (
    #     f'На объявление {ad_title} принят Ваш отклик.'
    #     f'Текст отклика: {text_response}'
    #     f'Ссылка на объявление: http://127.0.0.1:8000{ad.get_absolute_url()}'
    # )
    # html_content = (
    #     f'На объявление {ad_title} принят Ваш отклик.'
    #     f'Текст отклика: {text_response}'
    #     f'<a href="http://127.0.0.1{ad.get_absolute_url()}">'
    #     f'Ссылка на объявление</a>'
    # )
    #
    # msg = EmailMultiAlternatives(subject, text_content, None, [email])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()

    return redirect('user_profile', request.user.username)


@login_required
@csrf_protect
def delete_response(request, pk):
    logging.debug('delete response')
    response = Response.objects.get(id=pk)

    if response.ad.created_by != request.user:
        # Ответить на отклик может только автор объявления, даже если он сам оставил отклик
        return redirect('user_profile', request.user.username)

    # text_response = response.text
    response.delete()

    # email = response.created_by.email
    # ad = response.ad
    # ad_title = ad.title
    #
    # subject = f'Ваш отклик был удален'
    # text_content = (
    #     f'На объявление {ad_title} удален Ваш отклик.'
    #     f'Текст отклика: {text_response}'
    #     f'Ссылка на объявление: http://127.0.0.1:8000{ad.get_absolute_url()}'
    # )
    # html_content = (
    #     f'На объявление {ad_title} удален Ваш отклик.'
    #     f'Текст отклика: {text_response}'
    #     f'<a href="http://127.0.0.1{ad.get_absolute_url()}">'
    #     f'Ссылка на объявление</a>'
    # )
    #
    # msg = EmailMultiAlternatives(subject, text_content, None, [email])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()

    return redirect('user_profile', request.user.username)
