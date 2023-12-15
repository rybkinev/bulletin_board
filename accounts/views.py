import logging

from allauth.account.models import EmailAddress
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

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
