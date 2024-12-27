from rest_framework import serializers

from .models import PerevalAdd, Coords, PerevalUser

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""
    class Meta:
       model = PerevalUser
       fields = ['fam', 'name', 'otc', 'email', 'phone']

class CoordsSerializer(serializers.ModelSerializer):
    """Сериализатор координат перевала"""
    class Meta:
       model = Coords
       fields = ['latitude', 'longitude', 'height']


class PerevalAddSerializer(serializers.ModelSerializer):
    """Сериализатор перевалов"""
    user = serializers.PrimaryKeyRelatedField(queryset=PerevalUser.objects.all())
    coords = serializers.PrimaryKeyRelatedField(queryset=Coords.objects.all())

    class Meta:
        model = PerevalAdd
        depth = 1
        fields = ("beauty_title",
                  "title",
                  "other_titles",
                  "connect",
                  "add_time",
                  "user",
                  "coords",
                  "level_winter",
                  "level_summer",
                  "level_autumn",
                  "level_spring",
                  )

class PerevalDetailSerializer(serializers.ModelSerializer):
    """Сериализатор перевала(детальный)"""

    class Meta:
        model = PerevalAdd
        depth = 1
        fields = '__all__'

class AuthEmailPerevalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalAdd
        depth = 1
        fields = ("beauty_title",
                  "title",
                  "other_titles",
                  "connect",
                  "add_time",
                  "coords",
                  "level_winter",
                  "level_summer",
                  "level_autumn",
                  "level_spring",
                  )
