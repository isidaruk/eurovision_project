from django.contrib import admin

from .models import Participant


class ParticipantAdmin(admin.ModelAdmin):

    list_display = ('__str__', 'view_total_score', 'total_voted')
    list_filter = ('contest', 'contest__year', 'contest__host_country', )
    search_fields = ('contest__year', 'contest__host_country',)

    def view_total_score(self, obj):
        return obj.total_score

    view_total_score.empty_value_display = '0'
    view_total_score.short_description = 'Total score'

    def total_voted(self, obj):
        return "%s / %s" % (obj.voted_count, obj.count_total_participants)
    total_voted.short_description = 'Voted'


admin.site.register(Participant, ParticipantAdmin)
