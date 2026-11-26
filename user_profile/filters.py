import django_filters

from user_profile.models import Profile


class ProfileFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr="icontains")
    country = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Profile
        fields = ("city", "country")
