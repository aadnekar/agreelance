import django_filters

from projects.models import Project

class ProjectFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")
    class Meta:
        model = Project
        fields = ["title", "description"]
