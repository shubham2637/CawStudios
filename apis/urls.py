from django.urls import path, include
from rest_framework import routers

from .views import RegisterView, BookTicket, MovieView, CityView


router = routers.DefaultRouter()
router.register(r'city', CityView)

urlpatterns = [
    path('', include(router.urls)),
    path('bookticket/', BookTicket.as_view(), name='bookticket'),
    path('movie/', MovieView.as_view(), name='movie'),
    #path('city/', CityView.as_view(), name='city'),
    path('showByMovie/', BookTicket.as_view(), name='bookticket'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]