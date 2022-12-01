from django.db import models
from datetime import date

# Create your models here.

SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large')
    )

MONTHS = (
        (1, 'Styczeń'),
        (2, 'Luty'),
        (3, 'Marzec'),
        (4, 'Kwiecień'),
        (5, 'Maj'),
        (6, 'Czerwiec'),
        (7, 'Lipiec'),
        (8, 'Sierpień'),
        (9, 'Wrzesień'),
        (10, 'Październik'),
        (11, 'Listopad'),
        (12, 'Grudzień')
    )


class Team(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    country = models.CharField(max_length=2, null=False, blank=False)

    def __str__(self):
        return self.name


class Person(models.Model):
    class Meta:
        ordering = ['name']
        permissions = [
            ('can_view_other_persons', 'You can see persons from same team.'),
        ]

    name = models.CharField(max_length=30, null=False, blank=False)
    surname = models.CharField(max_length=30, null=False, blank=False)
    month_added = models.IntegerField(choices=MONTHS, default=date.today().month)
    date_added = models.DateField(auto_now_add=True)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES, default=SHIRT_SIZES[0][0])
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name




