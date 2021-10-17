from django.urls import path, include
from rest_framework import routers

from .views import RegisterView, BookTicket, MovieView, CityView, movieByCity, cinemaByShowtime, bookticket, \
    seatsByShowtime

router = routers.DefaultRouter()
router.register(r'city', CityView)
router.register(r'movie', MovieView)

urlpatterns = [
    path('', include(router.urls)),
    path('book/<city_name>/<movie_name>/<theatre_name>/<show_name>', bookticket, name="bookticket"),
    #path('movie/', MovieView.as_view(), name='movie'),
    path('movieByCity/<slug:city>', movieByCity, name='movieByCity'),
    path('cinemaByShowtime', cinemaByShowtime, name='cinemaByShowtime'),
    path('seatsByShowtime', seatsByShowtime, name='seatsByShowtime'),
    #path('city/', CityView.as_view(), name='city'),

    path('showByMovie/', BookTicket.as_view(), name='bookticket'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]