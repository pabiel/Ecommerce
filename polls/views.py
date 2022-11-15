from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person, Team
from .serializers import PersonSerializer, TeamSerializer

# lista akceptowanych metod protokołu HTTP, to pozwala na zgłaszanie wyjątków
# w przypadku próby dostępu metodą spoza listy


@api_view(['GET', 'POST'])
def person_list(request):
    """
    Lista wszystkich obiektów klasy Person.
    """
    if request.method == 'GET':
        persons = Person.objects.all()
        # dane podawane są poprzez uprzednio przygotowany serializer
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def person_detail(request, pk):
    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Person
    :return: Response (może zawierać dane i/lub status HTTP żądania)
    """
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        """
        Zwraca pojedynczy obiekt typu Person.
        """
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    elif request.method == 'PUT':
        """
        Aktualizacja obiekt typu Person.
        """
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        """
        Usuwanie obiektu typu Person.
        """
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_by_names(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        try:
            persons = Person.objects.filter(name__icontains=name)
            serializer = PersonSerializer(persons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def team_list(request):
    """
    Lista wszystkich obiektów klasy Team.
    """
    if request.method == 'GET':
        teams = Team.objects.all()
        # dane podawane są poprzez uprzednio przygotowany serializer
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def team_detail(request, pk):
    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Person
    :return: Response (może zawierać dane i/lub status HTTP żądania)
    """
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        """
        Zwraca pojedynczy obiekt typu Person.
        """
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    elif request.method == 'PUT':
        """
        Aktualizacja obiekt typu Person.
        """
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        """
        Usuwanie obiektu typu Person.
        """
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
