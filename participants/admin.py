from django.contrib import admin
from django.db.models import Sum
from django.db.models import Value as V
from django.db.models.functions import Coalesce
from django.utils.safestring import mark_safe

from .models import Participant


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'view_total_score', 'total_voted', 'cached_total_score', 'voted_ratio',)
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

    def cached_total_score(self, obj):
        return obj.cached_total_score

    cached_total_score.short_description = 'Cached total score'

    def voted_ratio(self, obj):
        if not obj.view_total_score:
            return mark_safe('<div style="width: 100px; height: 10px; border: 1px solid black"></div>')

        percent = int(obj.count_voted * 100.0 / obj.count_total_participants)
        return mark_safe('<div style="width: 100px; height: 10px; border: 1px solid black; background: #417690;">'
                         f'<div style="width: {percent}px; height: 10px; background: #f5dd5d;"></div>'
                         '</div>')

    voted_ratio.short_description = 'Votes ratio'


admin.site.register(Participant, ParticipantAdmin)
