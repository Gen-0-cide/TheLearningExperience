from django.contrib.auth.models import User, AbstractUser
from django.db import models

class PerevalUser(models.Model):
    """
    Класс модели для пользователей. Поля модели:
    email - уникальный адрес электронной почты;
    otc - отчество;
    phone - номер телефона.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fam = models.CharField(max_length=254, default=None, verbose_name="Фамилия")
    name = models.CharField(max_length=254, default=None,  verbose_name="Имя")
    email = models.EmailField(unique=True, default=None, verbose_name="Эл.почта")
    otc = models.CharField(max_length=255, verbose_name="Отчество")
    phone = models.CharField(max_length=64, verbose_name="Номер телефона")

    def __str__(self):
        return f'{self.fam} {self.name} {self.otc}'


class Coords(models.Model):
    """
    Класс модели для координат перевала.
    Поля модели:
    latitude - географическая широта;
    longitude - географическая долгота;
    height - высота над уровнем моря
    """
    latitude = models.FloatField(max_length=254, verbose_name="Широта")
    longitude = models.FloatField(max_length=254, verbose_name="Долгота")
    height = models.IntegerField(verbose_name="Высота")

    def __str__(self):
        return f'Широта - {self.latitude}. Долгота - {self.longitude}. Высота - {self.height} метров.'

    class Meta:
        verbose_name_plural = ("Координаты")


class PerevalAdd(models.Model):
    """Класс модели для перевала."""
    NEW, PENDING, ACCEPTED, REJECTED = 'N', 'P', 'A', 'R'
    STATUS_CHOICES = [(NEW, 'Новый'), (PENDING, 'Модерируется',), (ACCEPTED, 'Принят',), (REJECTED, 'Отклонен')]

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=NEW)
    beauty_title = models.CharField(max_length=254)
    title = models.CharField(max_length=254)
    other_titles = models.CharField(max_length=254)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")

    user = models.ForeignKey(PerevalUser, on_delete=models.CASCADE, related_name='pereval')
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    # Категории сложностей
    level_spring = models.CharField(max_length=254, blank=True, verbose_name="Сложность весной")
    level_summer = models.CharField(max_length=254, blank=True, verbose_name="Сложность летом")
    level_autumn = models.CharField(max_length=254, blank=True, verbose_name="Сложность осенью")
    level_winter = models.CharField(max_length=254, blank=True, verbose_name="Сложность зимой")

    def __str__(self):
        return f"id: {self.pk}, title:{self.title}"

class Images(models.Model):
    """
    Класс модели для загружаемых картинок(фотографий перевалов):
    Поля модели:
    title - Название фотографии;
    image - фото перевала (в виде необработанных двоичных данных);
    date_added - время добавления фото.
    pereval - перевал, который сфотографировали (связан с моделью PerevalAdd);
    """
    title = models.CharField(max_length=254, verbose_name="Название")
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    date_added = models.DateField(auto_now_add=True, verbose_name="Время добавления")

    pereval = models.ForeignKey(PerevalAdd, on_delete=models.CASCADE)

    def __str__(self):
        return f"id: {self.pk}, title:{self.title}"

    class Meta:
        verbose_name_plural = ("Фотографии")

