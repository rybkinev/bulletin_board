from django.views.generic import ListView

from board.models import Bulletin


class BoardView(ListView):
    model = Bulletin
    # ordering = '-created_at'
    template_name = 'board.html'
    # context_object_name = 'news'
    # paginate_by = 10
    # search = False
