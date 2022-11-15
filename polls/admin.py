from django.contrib import admin
from .models import Person
from .models import Team
from django.db.models.functions import Lower

# Register your models here.


class PersonAdmin(admin.ModelAdmin):
    class Meta:
        ordering = ['name']

    list_display = ['name', 'shirt_size', 'get_full_team']
    list_filter = ['team', 'date_added']

    @admin.display
    def get_full_team(self, obj):
        if obj.team is not None:
            return f"{obj.team.name} ({obj.team.country})"
        return "---"

    def get_ordering(self, request):
        return [Lower('name')]  # sort case-insensitive


admin.site.register(Person, PersonAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    list_filter = ['country']


admin.site.register(Team, TeamAdmin)
