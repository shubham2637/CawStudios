import datetime
import logging

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.models import Movie, City, Show, MovieTheatreShow, Ticket, Booking, Payment
from apis.serializers import RegisterSerializer, CitySerializer, ShowSerializer, CinemaSerializer, MovieSerializer, \
    BookingSerializer

logging.basicConfig( filename='api.log',
                     level=logging.INFO,
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


@api_view( ['GET'] )
def movie_by_city(request):
    try:
        try:
            city = request.POST['city']
        except Exception as e:
            message = str( e )
            httpStatus = status.HTTP_400_BAD_REQUEST
            return Response( message, status=httpStatus )
        try:
            movie_details = MovieTheatreShow.objects.filter( cinema__address__city=city ).prefetch_related( 'movie' )
            movie_detailsList = []
            if movie_details:
                for movie_detailsObj in movie_details:
                    movie_detailsList.append( MovieSerializer( movie_detailsObj.movie ).data )
        except Exception as e:
            message = str( e )
            return Response( message, status=status.HTTP_409_CONFLICT )
    except Exception as e:
        message = str( e )
        return Response( message, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
    if movie_details:
        return Response( {"movies": movie_detailsList}, status.HTTP_200_OK )
    return Response( {"movies": "No movies in the city"}, status.HTTP_200_OK )


@api_view( ['GET'] )
def cinemaByShowtime(request):
    try:
        try:
            showtime = request.POST['showtime']
        except Exception as e:
            message = str( e )
            httpStatus = status.HTTP_400_BAD_REQUEST
            return Response( message, status=httpStatus )
        try:
            movie_details = MovieTheatreShow.objects.filter( show__name=showtime ).values( 'movie__Title', 'show__name',
                                                                                           'show__available_seats' )
        except Exception as e:
            message = str( e )
            return Response( message, status=status.HTTP_409_CONFLICT )
    except Exception as e:
        message = str( e )
        return Response( message, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
    if movie_details:
        return Response( {"seats": movie_details}, status.HTTP_200_OK )
    return Response( {"movies": "No movies in the city"}, status.HTTP_200_OK )


@api_view( ['GET'] )
def seatsByShowtime(request):
    try:
        showtime_id = request.POST.get( 'showtime_id' )
        shows = Show.objects.filter().prefetch_related( 'cinema' ).values( 'ticket__price', 'total_seats',
                                                                           'available_seats', 'cinema__name' )
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


@api_view( ['POST'] )
@permission_classes((IsAuthenticated, ))
def bookticket(request):
    try:
        try:
            user = request.user
            ticket_id = request.POST['ticket_id']
            Moviedetails_id = request.POST['Moviedetails_id']
            mode_of_payment = request.POST['mode_of_payment']
            amount = request.POST['amount']
        except Exception as e:
            message = str( e )
            httpStatus = status.HTTP_400_BAD_REQUEST
            return Response( message, status=httpStatus )
        try:
            ticket = Ticket.objects.get( pk=ticket_id )
            moviedetails = MovieTheatreShow.objects.get( pk=Moviedetails_id )
            booking = Booking( user=user, ticket=ticket, moviedetails=moviedetails, status='INITIATED' )
            booking.save()
            #Saved Booking info
            #Assuming a payment Gateway API call

            payment = Payment(booking=booking,mode_of_payment=mode_of_payment,amount=amount)
            booking.status = "DONE"
            payment.save()
            booking.save()
            context = {
                "response" : "Booking Initiated",
                "booking_details" : {
                    "booking_id" : booking.pk,
                    "payment_id" : payment.pk,
                    "status": booking.status,
                    "user": user.username,
                    "ticket": ticket.category+" " + str(ticket.price),
                    "moviedetails": moviedetails.movie.Title + moviedetails.show.name
                }
            }
        except Exception as e:
            message = str( e )
            return Response( message, status=status.HTTP_404_NOT_FOUND )
    except Exception as e:
        message = str( e )
        return Response( message, status=status.HTTP_500_INTERNAL_SERVER_ERROR )
    return Response( context, status.HTTP_201_CREATED )
