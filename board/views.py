from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView

from board.forms import BulletinForm
from board.models import Bulletin


class BoardView(ListView):
    model = Bulletin
    ordering = '-created_at'
    template_name = 'board_list.html'
    context_object_name = 'bulletins'
    # paginate_by = 10
    # search = False


class BulletinCreateView(CreateView):
    form_class = BulletinForm
    model = Bulletin
    template_name = 'bulletin_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.created_by = self.request.user

        return super(BulletinCreateView, self).form_valid(form)
