from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import generics, viewsets, mixins
from .serializers import *

class PerevalAddAPI(generics.CreateAPIView):
    """Класс работы с БД для первого спринта"""
    queryset = PerevalAdd.objects.all()
    serializer_class = PerevalAddSerializer

    def post(self, request):
        """
        Переопределение метода POST
        """
        pereval = PerevalAddSerializer(data=request.data)
        try:
            if pereval.is_valid(raise_exception=True):
                pereval.save()
                data = {'status': '200', 'message': 'null', 'id': f'{pereval.instance.id}'}
                return JsonResponse(data, status=200, safe=False)

        except Exception as exc:
            responseData = {'status': '400', 'message': f'Bad Request: {exc}', 'id': 'null'}
            return JsonResponse(responseData, status=400, safe=False)


class PerevalDetailAPI(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """Класс работы с БД для второго спринта: извлечение и редактирование перевала"""
    queryset = PerevalAdd.objects.all()
    serializer_class = PerevalDetailSerializer

    def update(self, request, *args, **kwargs):
        """
        Переопределение метода update(PATCH)
        """
        pk = kwargs.get("pk", None)

        try:
            instance = PerevalAdd.objects.get(pk=pk)
        except:
            return Response({"error": "Такого перевала не существует"}, status=400)

        if instance.status != "N":
            return Response({"message": "Перевал на модерации, вы не можете его изменить",
                             "state": 0}, status=400)
        else:
            serializer = PerevalDetailSerializer(data=request.data, instance=instance)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"state": 1}, status=200)


class AuthEmailPerevalAPI(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Класс работы с БД для второго спринта: вывод всех записей по email"""
    queryset = PerevalAdd.objects.all()
    serializer_class = AuthEmailPerevalSerializer

    def get(self, request, *args, **kwargs):
        """
        Переопределение метода GET для вывода всех записей по email
        :param request: Json для полей модели перевала (PerevalAdd)
        :return: Response пример: { "status": 200, "message": null, "id": 42 }
        """
        email = kwargs.get('email', None)
        if PerevalAdd.objects.filter(user__email=email).is_exist == True:
            responseData = AuthEmailPerevalSerializer(PerevalAdd.objects.filter(user__email=email), many=True).data

        else:
            responseData = {'message': f'Нет записей от email = {email}'}

        return Response(responseData, status=200)
