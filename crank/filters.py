from .models import Rating_id
import django_filters

class RatingFilter(django_filters.FilterSet):
    class Meta:
        model = Rating_id
        fields = ['uni', 'course', 'overall_quality']

