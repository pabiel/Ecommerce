from django.shortcuts import render
from .models import Person, Team
from .serializers import PersonSerializer, TeamSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission

# lista akceptowanych metod protokołu HTTP, to pozwala na zgłaszanie wyjątków
# w przypadku próby dostępu metodą spoza listy

# SAFE_METHODS = ['GET']


# class IsAuthenticatedOrReadOnly(BasePermission):
#     def has_premission(self, request, view):
#         if request.method in SAFE_METHODS or request.user and request.user.is_authenticated():
#             return True
#         return False


class PersonList(APIView):
    """
    Wylistuj wszystkich obiekty, lub stwórz obiekty klasy Person.
    """
    def get(self, request, format=None):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        person = self.get_object(pk)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        person = self.get_object(pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetByName(ListAPIView):
    serializer_class = PersonSerializer

    def get_queryset(self):
        # if self.request.method == 'GET':
        name = self.request.query_params.get('name')
        queryset = Person.objects.filter(name__icontains=name)
        return queryset


@api_view(['GET'])
def team_list(request):
    """
    Lista wszystkich obiektów klasy Team.
    """
    if request.method == 'GET':
        teams = Team.objects.all()
        # dane podawane są poprzez uprzednio przygotowany serializer
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def team_detail(request, pk):
    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Team
    :return: Response (może zawierać dane i/lub status HTTP żądania)
    """
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        """
        Zwraca pojedynczy obiekt typu Team.
        """
        serializer = TeamSerializer(team)
        return Response(serializer.data)


@api_view(['POST', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def team_create_update_delete(request, pk):
    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Team
    :return: Response (może zawierać dane i/lub status HTTP żądania)
    """
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        """
        Aktualizacja obiekt typu Team.
        """
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        """
        Usuwanie obiektu typu Team.
        """
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
