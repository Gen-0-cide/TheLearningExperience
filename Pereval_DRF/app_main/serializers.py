from rest_framework import serializers
from .models import PerevalAdd, Coords, PerevalUser , Images

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

class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображений"""
    class Meta:
        model = Images
        fields = ['title', 'image']

class PerevalAddSerializer(serializers.ModelSerializer):
    """Сериализатор перевалов"""
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = PerevalAdd
        fields = (
            "beauty_title",
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
            "images",
        )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images')

        # Создаем пользователя
        user_instance = PerevalUser .objects.create(**user_data)

        # Создаем координаты
        coords_instance = Coords.objects.create(**coords_data)

        # Создаем перевал
        pereval_instance = PerevalAdd.objects.create(user=user_instance, coords=coords_instance, **validated_data)

        # Создаем изображения и связываем их с перевалом
        for image_data in images_data:
            Images.objects.create(pereval=pereval_instance, **image_data)

        return pereval_instance

class PerevalDetailSerializer(serializers.ModelSerializer):
    """Сериализатор перевала (детальный)"""
    class Meta:
        model = PerevalAdd
        depth = 1
        fields = '__all__'

class AuthEmailPerevalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerevalAdd
        depth = 1
        fields = (
            "beauty_title",
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

