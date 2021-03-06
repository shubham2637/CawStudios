from datetime import datetime, time

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class City(models.Model):
    city = models.CharField( max_length=20 )
    state = models.CharField( max_length=20 )
    pincode = models.CharField( max_length=6 )

    def __str__(self):
        return f"{self.id} {self.city} {self.state} {self.pincode}"


class Cinema(models.Model):
    name = models.CharField( max_length=64 )
    address = models.ForeignKey( City, on_delete=models.CASCADE )

    def __str__(self):
        return f"{self.id} {self.name} {self.address.city} "


class Movie(models.Model):
    Title = models.CharField( max_length=20, unique=True )
    Description = models.CharField( max_length=20 )
    Genre = models.CharField( max_length=20 )
    Language = models.CharField( max_length=20 )
    CountryOfOrigin = models.CharField( max_length=20 )
    Duration = models.IntegerField( default=90 )
    rating = models.IntegerField( default=7 )

    def __str__(self):
        return f"{self.id} {self.Title} {self.rating}"


class Show(models.Model):
    name = models.CharField( max_length=20, unique=True )
    timestamp = models.DateTimeField( auto_now_add=True )
    start_time = models.TimeField( default='09:00', blank=False )
    end_time = models.TimeField( default='11:00', blank=False )
    total_seats = models.IntegerField( default=20 )
    available_seats = models.IntegerField( default=20 )

    def __str__(self):
        return f"{self.id} {self.name} {self.start_time} left seat : {self.available_seats}"


class Ticket(models.Model):
    category = models.CharField( max_length=20)
    show = models.ForeignKey( Show, on_delete=models.CASCADE )
    price = models.DecimalField( decimal_places=2, max_digits=8 )

    class Meta:
        unique_together = ['category','show']

    def __str__(self):
        return f"{self.id} {self.price} {self.show.name} {self.category} "

class MovieCinemaShow( models.Model ):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.today)

    def __str__(self):
        return f"{self.id} {self.movie.Title} at {self.cinema.name} {self.cinema.address.city} {self.date} "

class Booking(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE )
    ticket = models.ForeignKey( Ticket, on_delete=models.CASCADE )
    moviedetails = models.ForeignKey( MovieCinemaShow, on_delete=models.CASCADE )
    timestamp = models.DateTimeField( auto_now_add=True )
    status = models.CharField( max_length=10 )

    def __str__(self):
        return f"{self.id} {self.user.username} {self.moviedetails.movie.Title} {self.ticket.show.start_time} INR{self.ticket.price} "


class Payment(models.Model):
    booking = models.ForeignKey( Booking, on_delete=models.CASCADE )
    timestamp = models.DateTimeField( auto_now_add=True )
    amount = models.DecimalField( decimal_places=2, max_digits=8 )
    mode_of_payment = models.CharField( max_length=10 , default='CASH')

    def __str__(self):
        return f"{self.id} {self.booking.moviedetails.movie.Title} {self.amount} {self.timestamp}"
