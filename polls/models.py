import datetime
from django.db import models
from django.utils import timezone


# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Team(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    country = models.CharField(max_length=2, null=False, blank=False)

    def __str__(self):
        return self.name


class Person(models.Model):

    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )

    imie = models.CharField(max_length=30, null=False, blank=False)
    nazwisko = models.CharField(max_length=30, null=False, blank=False)
    miesiac_urodzenia = models.IntegerChoices('miesiac_urodzenia', 'styczeń luty marzec kwiecień maj czerwiec lipiec '
                                                                   'sierpień wrzesień październik listopad grudzień')
    miesiac = models.IntegerField(blank=False, choices=miesiac_urodzenia.choices,
                                  default=miesiac_urodzenia.choices[0])
    data_dodania = models.DateField(auto_now_add=True)
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL, default=0)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

    def __str__(self):
        return self.imie

    class Meta:
        ordering = ['imie']


