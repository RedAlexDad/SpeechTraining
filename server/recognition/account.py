from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import authenticate
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from recognition.permissions import IsModerator, IsAuthenticated, create_access_token, \
    get_jwt_payload, get_access_token, add_in_blacklist

from recognition.serializers import AccountSerializer, AccountSerializerInfo, AccountAuthorizationSerializer, AccountRegisterSerializer
from recognition.models import Account

# ==================================================================================
# АККАУНТЫ
# ==================================================================================
from rest_framework import status
from django.shortcuts import get_object_or_404


class AccountGET(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]
    model_class = Account
    serializer_class = AccountSerializer

    def get(self, request, format=None):
        print('[INFO] API GET [accountsINFO]')
        accounts = self.model_class.objects.all()
        serializer = self.serializer_class(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountPUT(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsModerator]
    model_class = Account
    serializer_class = AccountRegisterSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def put(self, request, pk, format=None):
        print('[INFO] API PUT [accountsINFO]')
        accounts = get_object_or_404(self.model_class, pk=pk)
        serializer = self.serializer_class(accounts, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDELETE(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsModerator]
    model_class = Account

    def delete(self, request, pk, format=None):
        print('[INFO] API DELETE [accountsINFO]')
        accounts = get_object_or_404(self.model_class, pk=pk)
        accounts.delete()
        return Response(data={'message': 'Успешно'}, status=status.HTTP_204_NO_CONTENT)

# ==================================================================================
# РЕГИСТРАЦИЯ, АУТЕНФИКАЦИЯ, ПОЛУЧЕНИЕ ТОКЕНА, ВЫХОД С УЧЕТНОЙ ЗАПИСИ
# ==================================================================================
# Регистрация
class RegisterView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = []

    @swagger_auto_schema(request_body=AccountRegisterSerializer)
    def post(self, request):
        try:
            # Получаем данные пользователя из запроса
            account_data = {
                "username": request.data.get("username"),
                "password": request.data.get("password"),
                "is_moderator": request.data.get("is_moderator", False),
                "name": request.data.get("name"),
                "lastname": request.data.get("lastname"),
                "fathername": request.data.get("fathername"),
            }
            # Сериализуем данные пользователя и сохраняем их
            account_serializer = AccountRegisterSerializer(data=account_data)
            account_serializer.is_valid(raise_exception=True)
            account_instance = account_serializer.save()
            # Возвращаем успешный ответ с данными пользователя
            return Response(data=account_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as error:
            # Обработка и возврат ошибки
            return Response(data={"message": str(error)}, status=status.HTTP_400_BAD_REQUEST)


# Аутентификация
class LoginView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=AccountAuthorizationSerializer)
    def post(self, request):
        try:
            # Проверяем данные пользователя
            account_serializer = AccountAuthorizationSerializer(data=request.data)
            account_serializer.is_valid(raise_exception=True)

            # Аутентификация пользователя
            account = authenticate(**account_serializer.validated_data)
            if account is None:
                return Response({'message': 'Такого аккаунта не найдено. Проверьте свои учетные данные'},
                                status=status.HTTP_401_UNAUTHORIZED)

            # Создание токена доступа
            error_message, access_token = create_access_token(account)

            # Получение данных аккаунта
            account_instance = Account.objects.get(id=account.id)
            account_serializer = AccountSerializer(account_instance)

            # Формирование ответа
            response_data = account_serializer.data
            if error_message:
                response_data['error_message'] = error_message

            # Установка cookie с токеном доступа
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(key='access_token', value=access_token, httponly=True)

            return response

        except Exception as error:
            return Response(data={"message": str(error)}, status=status.HTTP_400_BAD_REQUEST)


# Получение токена
class GetToken(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = []

    def post(self, request):
        error_message, access_token = get_access_token(request)

        if access_token is None:
            return Response(error_message, status=status.HTTP_401_UNAUTHORIZED)
        payload = get_jwt_payload(access_token)
        account = Account.objects.filter(id=payload['id']).first()

        data = {
            'account': AccountSerializerInfo(account, many=False).data,
            'message': 'Успешно',
            'access_token': access_token,
        }
        # Добавляем error_message, если есть ошибка
        if error_message:
            data['error_message'] = error_message

        return Response(data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = []

    def post(self, request):
        access_token = request.COOKIES.get('access_token')

        # Проверка наличия токена
        if access_token is None:
            return Response({'message': 'Токен в access_token и cookie не найден. Мы, может быть, уже вышли из системы?'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Добавление токена в черный список в Redis
        error_message, token_exists = add_in_blacklist(access_token)
        response = Response(status=status.HTTP_200_OK)

        # Удаление куки с токеном
        response.delete_cookie('access_token')
        response.data = {
            'message': 'Успешно',
            'is_token_in_blacklist': bool(token_exists)
        }

        # Добавляем error_message, если есть ошибка
        if error_message:
            response.data['error_message'] = error_message

        return response
