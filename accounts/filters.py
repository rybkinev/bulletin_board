from django_filters import FilterSet

from board.models import Ad


class AdFilter(FilterSet):
    class Meta:
        model = Ad
        fields = {
            'title': ['icontains'],
        }
