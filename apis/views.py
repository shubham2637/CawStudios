from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import Movie, City
from apis.serializers import RegisterSerializer, MovieSerializer, CitySerializer


class BookTicket(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class CityView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_fields = ('city', 'state')

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = City.objects.all()
        city = self.request.QUERY_PARAMS.get('city', None)
        if city is not None:
            queryset = queryset.filter(city=city)
        return queryset

class MovieView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer