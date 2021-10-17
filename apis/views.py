import datetime
import logging

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import Movie, City, Show
from apis.serializers import RegisterSerializer, MovieSerializer, CitySerializer, ShowSerializer, CinemaSerializer

logging.basicConfig( filename='api.log',
                     level=logging.DEBUG,
                     format='%(asctime)s - %(name)s - %(threadName)s -  %(levelname)s - %(message)s' )


class BookTicket( APIView ):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response( content )


class RegisterView( generics.CreateAPIView ):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class CityView( viewsets.ModelViewSet ):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_fields = ('city', 'state')

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = City.objects.all()
        city = self.request.query_params.get( 'city' )
        if city:
            queryset = queryset.filter( city=city )
        return queryset


class MovieView( viewsets.ModelViewSet ):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_fields = ('title', 'genre', 'language', 'city')

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Movie.objects.all()
        city = self.request.query_params.get( 'city' )
        genre = self.request.query_params.get( 'genre' )
        language = self.request.query_params.get( 'language' )
        title = self.request.query_params.get( 'title' )
        if city:
            queryset = Show.objects.filter( cinema__address__city=city ).prefetch_related( 'movie' ).values( 'movie' )
        return queryset


@api_view( ['GET'] )
def movieByCity(request, city):
    try:
        shows = Show.objects.filter( cinema__address__city=city ).prefetch_related( 'movie' )
        if shows:
            movieList = []
            for show in shows:
                movieList.append( MovieSerializer( show.movie ).data )
            logging.log( level=1, msg=status.HTTP_200_OK )
            return Response( movieList, status.HTTP_200_OK )
        else:
            message = "City not found "
            httpStatus = status.HTTP_400_BAD_REQUEST
            return Response( message, status=httpStatus )
    except Exception as e:
        message = str( e )
        logging.exception( message )
        httpStatus = status.HTTP_400_BAD_REQUEST
        return Response( message, status=httpStatus )


@api_view( ['GET'] )
def cinemaByShowtime(request):
    try:
        showtime = request.POST.get( 'showtime')
        shows = Show.objects.filter( name=showtime ).prefetch_related('cinema')
        showData = []
        if shows:
            for s in shows:
                showData.append( CinemaSerializer( s.cinema ).data )
            logging.log( level=1, msg=status.HTTP_200_OK )
            return Response( showData, status.HTTP_200_OK )
        else:
            message = {"res": "Invalid Showtime"}
            logging.exception( message )
            httpStatus = status.HTTP_400_BAD_REQUEST
            return Response( message, status=httpStatus )
    except Exception as e:
        message = str( e )
        logging.exception( message )
        httpStatus = status.HTTP_400_BAD_REQUEST
        return Response( message, status=httpStatus )
@api_view( ['GET'] )
def seatsByShowtime(request):
    try:
        showtime_id = request.POST.get( 'showtime_id')
        shows = Show.objects.filter(  ).prefetch_related('cinema').values('ticket__price','total_seats','available_seats','cinema__name')
        ticketDetails = []
        if shows:
            logging.log( level=1, msg=status.HTTP_200_OK )
            return Response( shows, status.HTTP_200_OK )
        else:
            message = {"res": "Invalid Showtime"}
            logging.exception( message )
            httpStatus = status.HTTP_400_BAD_REQUEST
            return Response( message, status=httpStatus )
    except Exception as e:
        message = str( e )
        logging.exception( message )
        httpStatus = status.HTTP_400_BAD_REQUEST
        return Response( message, status=httpStatus )


@api_view( ['GET'] )
def bookticket(request, movie):
    pass
