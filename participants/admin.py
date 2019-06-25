from django.contrib import admin
from django.db.models import Sum
from django.db.models import Value as V
from django.db.models.functions import Coalesce

from .models import Participant


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'view_total_score', 'total_voted',)
    list_filter = ('contest', 'contest__year', 'contest__host_country',)
    search_fields = ('contest__year', 'contest__host_country__name',)

    def get_queryset(self, request):
        qs = super(ParticipantAdmin, self).get_queryset(request)
        return qs.annotate(view_total_score=Coalesce(Sum('votes__point'), V(0)))

    def view_total_score(self, obj):
        return obj.view_total_score

    view_total_score.short_description = 'Total score'
    view_total_score.admin_order_field = 'view_total_score'

    def total_voted(self, obj):
        return "%s / %s" % (obj.count_voted, obj.count_total_participants)

    total_voted.short_description = 'Voted'


admin.site.register(Participant, ParticipantAdmin)
