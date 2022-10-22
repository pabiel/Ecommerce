from django.contrib import admin
from .models import Question
from .models import Person
from .models import Team
from django.db.models.functions import Lower
# Register your models here.

admin.site.register(Question)


class PersonAdmin(admin.ModelAdmin):
    list_display = ['imie', 'shirt_size', 'get_full_team']
    list_filter = ['team', 'data_dodania']

    @admin.display
    def get_full_team(self, obj):
        if obj.team is not None:
            return f"{obj.team.name} ({obj.team.country})"
        return "---"

    def get_ordering(self, request):
        return [Lower('imie')]  # sort case insensitive

    class Meta:
        ordering = ['imie']


admin.site.register(Person, PersonAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    list_filter = ['country']


admin.site.register(Team, TeamAdmin)
