from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apis.models import Movie, City, Show, Cinema, Booking


class RegisterSerializer( serializers.ModelSerializer ):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator( queryset=User.objects.all() )]
    )

    password = serializers.CharField( write_only=True, required=True, validators=[validate_password] )
    password2 = serializers.CharField( write_only=True, required=True )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError( {"password": "Password fields didn't match."} )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password( validated_data['password'] )
        user.save()

        return user


class MovieSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Movie
        fields = '__all__'


class CitySerializer( serializers.ModelSerializer ):
    class Meta:
        model = City
        fields = '__all__'

class ShowSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Show
        fields = '__all__'

class CinemaSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Cinema
        fields = '__all__'

class BookingSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Booking
        fields = '__all__'
