from django.urls import path
from .views import RegisterView, BookTicket

urlpatterns = [
    path('bookticket/', BookTicket.as_view(), name='bookticket'),
    path('movieByCity/', BookTicket.as_view(), name='bookticket'),
    path('showByMovie/', BookTicket.as_view(), name='bookticket'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]