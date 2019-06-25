from django.db import models
from django.contrib import admin

from .models import Participant


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'view_total_score', 'total_voted',)
    list_filter = ('contest', 'contest__year', 'contest__host_country',)
    search_fields = ('contest__year', 'contest__host_country__name',)

    def get_queryset(self, request):
        qs = super(ParticipantAdmin, self).get_queryset(request)
        return qs.annotate(view_total_score=models.Sum('votes__point'))

    def view_total_score(self, obj):
        return obj.view_total_score  # or 0

    view_total_score.empty_value_display = '0'
    view_total_score.short_description = 'Total score'
    view_total_score.admin_order_field = 'view_total_score'

    def total_voted(self, obj):
        return "%s / %s" % (obj.count_voted, obj.count_total_participants)
    total_voted.short_description = 'Voted'


admin.site.register(Participant, ParticipantAdmin)
