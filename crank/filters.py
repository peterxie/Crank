from .models import Rating_id, Rating_Average
import django_filters

class RatingFilter(django_filters.FilterSet):
    class Meta:
        model = Rating_id
        fields = ['course_faculty', 'overall_quality']

class RatingAverageFilter(django_filters.FilterSet):
    class Meta:
        model = Rating_Average
        fields = ['overall_quality']
