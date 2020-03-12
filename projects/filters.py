import django_filters

from projects.models import Project
from django.db.models import Q


class ProjectFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name="search",
        lookup_expr="icontains",
        method="custom_filter")

    class Meta:
        model = Project
        fields = ["search"]

    def custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value))
