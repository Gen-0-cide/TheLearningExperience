from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import PerevalUser , Coords, PerevalAdd, Images

class PerevalUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.pereval_user = PerevalUser .objects.create(
            user=self.user,
            fam='Иванов',
            name='Иван',
            email='ivanov@example.com',
            otc='Иванович',
            phone='1234567890'
        )

    def test_pereval_user_creation(self):
        self.assertEqual(self.pereval_user.fam, 'Иванов')
        self.assertEqual(self.pereval_user.name, 'Иван')
        self.assertEqual(self.pereval_user.email, 'ivanov@example.com')
        self.assertEqual(self.pereval_user.phone, '1234567890')

    def test_str_method(self):
        self.assertEqual(str(self.pereval_user), 'Иванов Иван Иванович')


class CoordsModelTest(TestCase):
    def setUp(self):
        self.coords = Coords.objects.create(latitude=45.0, longitude=90.0, height=1000)

    def test_coords_creation(self):
        self.assertEqual(self.coords.latitude, 45.0)
        self.assertEqual(self.coords.longitude, 90.0)
        self.assertEqual(self.coords.height, 1000)

    def test_str_method(self):
        self.assertEqual(str(self.coords), 'Широта - 45.0. Долгота - 90.0. Высота - 1000 метров.')


class PerevalAddModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.pereval_user = PerevalUser .objects.create(
            user=self.user,
            fam='Иванов',
            name='Иван',
            email='ivanov@example.com',
            otc='Иванович',
            phone='1234567890'
        )
        self.coords = Coords.objects.create(latitude=45.0, longitude=90.0, height=1000)
        self.pereval_add = PerevalAdd.objects.create(
            status=PerevalAdd.NEW,
            beauty_title='Прекрасный перевал',
            title='Перевал 1',
            other_titles='Перевал 1',
            connect='Описание перевала',
            user=self.pereval_user,
            coords=self.coords
        )

    def test_pereval_add_creation(self):
        self.assertEqual(self.pereval_add.title, 'Перевал 1')
        self.assertEqual(self.pereval_add.status, PerevalAdd.NEW)

    def test_str_method(self):
        self.assertEqual(str(self.pereval_add), f"id: {self.pereval_add.pk}, title: {self.pereval_add.title}")


class ImagesModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.pereval_user = PerevalUser .objects.create(
            user=self.user,
            fam='Иванов',
            name='Иван',
            email='ivanov@example.com',
            otc='Иванович',
            phone='1234567890'
        )
        self.coords = Coords.objects.create(latitude=45.0, longitude=90.0, height=1000)
        self.pereval_add = PerevalAdd.objects.create(
            status=PerevalAdd.NEW,
            beauty_title='Прекрасный перевал',
            title='Перевал 1',
            other_titles='Перевал 1',
            connect='Описание перевала',
            user=self.pereval_user,
            coords=self.coords
        )
        self.image = Images.objects.create(
            title='Фото перевала',
            image='path/to/image.jpg',  # Укажите путь к тестовому изображению
            pereval=self.pereval_add
        )

    def test_images_creation(self):
        self.assertEqual(self.image.title, 'Фото перевала')

    def test_str_method(self):
        self.assertEqual(str(self.image), f"id: {self.image.pk}, title: {self.image.title}")

        
#class AuthEmailPerevalAPITest(TestCase):
#    def setUp(self):
#       self.pereval_user = PerevalUser .objects.create(
#            user=self.user,
#            fam='Иванов',
#            name='Иван',
#            email='ivanov@example.com',
#            otc='Иванович',
#            phone='1234567890'
#        )
#        self.coords = Coords.objects.create(latitude=45.0, longitude=90.0, height=1000)
#        self.pereval_add = PerevalAdd.objects.create(
#            status=PerevalAdd.NEW,
#            beauty_title='Прекрасный перевал',
#            title='Перевал 1',
#            other_titles='Перевал 1',
#            connect='Описание перевала',
#            user=self.pereval_user,
#            coords=self.coords
#        )
#
#    def test_get_perevals_by_email_success(self):
#        """Тест успешного получения перевалов по email."""
#        url = reverse('auth-email-pereval')
#        response = self.client.get(url, {'user__email': 'ivanov@example.com'})
#        self.assertEqual(response.status_code, status.HTTP_200_OK)
#        self.assertIn('data', response.data)
#        self.assertEqual(len(response.data['data']), 1)
#
#    def test_get_perevals_by_email_not_found(self):
#        """Тест получения перевалов по email, когда email не существует."""
#        url = reverse('auth-email-pereval')
#        response = self.client.get(url, {'user__email': 'nonexistent@example.com'})
#        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#        self.assertEqual(response.data['message'], 'Нет записей от email = nonexistent@example.com')
#
#    def test_get_perevals_by_email_no_email(self):
#        """Тест получения перевалов без указания email."""
#        url = reverse('auth-email-pereval')
#        response = self.client.get(url)
#        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#        self.assertEqual(response.data['message'], 'Email не указан')
