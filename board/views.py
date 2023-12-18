from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from board.forms import BulletinForm
from board.models import Bulletin


class BoardView(ListView):
    model = Bulletin
    ordering = '-created_at'
    template_name = 'board_list.html'
    context_object_name = 'bulletins'
    # paginate_by = 10
    # search = False


class BulletinCreateView(LoginRequiredMixin, CreateView):
    form_class = BulletinForm
    model = Bulletin
    template_name = 'bulletin_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.created_by = self.request.user

        return super(BulletinCreateView, self).form_valid(form)


class BulletinEditView(LoginRequiredMixin, UpdateView):
    form_class = BulletinForm
    model = Bulletin
    template_name = 'bulletin_edit.html'

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.created_by = self.request.user
    #
    #     return super(BulletinEditView, self).form_valid(form)


class BulletinDetailView(DetailView):
    model = Bulletin
    template_name = 'bulletin_detail.html'
    context_object_name = 'bulletin'
