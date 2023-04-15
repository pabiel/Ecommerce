from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .models import Person, Team
from .serializers import PersonSerializer, TeamSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# lista akceptowanych metod protokołu HTTP, to pozwala na zgłaszanie wyjątków
# w przypadku próby dostępu metodą spoza listy

# SAFE_METHODS = ['GET']


# class IsAuthenticatedOrReadOnly(BasePermission):
#     def has_premission(self, request, view):
#         if request.method in SAFE_METHODS or request.user and request.user.is_authenticated():
#             return True
#         return False



for user in User.objects.all():
    Token.objects.get_or_create(user=user)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def person_list(request):
    """
    Wylistuj wszystkich obiekty, lub stwórz obiekty klasy Person.
    """
    if request.method == 'GET':
        persons = Person.objects.filter(owner_id=request.user.id)
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def person_detail(request, pk):
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



@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_by_names(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        try:
            persons = Person.objects.filter(name__icontains=name)
            serializer = PersonSerializer(persons, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def person_create(request, pk):
    # try:
    #     person = Person.objects.get(pk=pk)
    # except Person.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        """
        Tworzenie obiektu typu Team.
        """
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def person_update(request, pk):
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        """
        Aktualizacja obiektu typu Person.
        """
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def person_delete(request, pk):
    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Person
    :return: Response (with status and/or object/s data)
    """
    try:
        person = Person.objects.get(pk=pk)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        """
        Usuwanie obiektu typu Person.
        """
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def teams_members(request, pk):
    if request.method == 'GET':
        persons = Person.objects.filter(team_id=pk, owner_id=request.user.id)
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def team_create(request, pk):
    if request.method == 'POST':
        """
        Tworzenie obiektu typu Team.
        """
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def team_update(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        """
        Aktualizacja obiektu typu Team.
        """
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def team_delete(request, pk):
    """
    :param request: obiekt DRF Request
    :param pk: id obiektu Team
    :return: Response (może zawierać dane i/lub status HTTP żądania)
    """
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        """
        Usuwanie obiektu typu Team.
        """
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


