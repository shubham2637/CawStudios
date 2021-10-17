from django.urls import path, include, re_path
from rest_framework import routers

from .views import RegisterView, BookTicket, CityView, cinemaByShowtime, bookticket, \
    seatsByShowtime, movie_by_city

router = routers.DefaultRouter()
router.register(r'city', CityView)

urlpatterns = [
    path('', include(router.urls)),
    re_path('bookticket', bookticket, name="bookticket"),
    #path('movie/', MovieView.as_view(), name='movie'),
    path('movieByCity', movie_by_city, name='movieByCity'),
    path('cinemaByShowtime', cinemaByShowtime, name='cinemaByShowtime'),
    path('seatsByShowtime', seatsByShowtime, name='seatsByShowtime'),
    #path('city/', CityView.as_view(), name='city'),

    path('showByMovie/', BookTicket.as_view(), name='bookticket'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]