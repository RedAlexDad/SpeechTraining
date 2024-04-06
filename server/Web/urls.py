"""Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from recognition.recognition_speech_automatic import TranscriptionView
from recognition import account
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),

    # Распознавание речи
    # path('api/transcribe/', TranscriptionView.as_view(), name='transcribe'),
]

# Авторизация, аутентификация, регистрация, выход с учетной записи
urlpatterns += [
    # Список аккаунтов
    path(r'api/users/', account.AccountGET.as_view()),
    # Обновление аккаунта
    path(r'api/users/<int:pk>/update/', account.AccountPUT.as_view()),
    # Удаление аккаунта
    path(r'api/users/<int:pk>/delete/', account.AccountDELETE.as_view()),

    # Регистрация
    path('api/register/', account.RegisterView.as_view()),
    # Аутентификация
    path('api/authentication/', account.LoginView.as_view()),
    # Получение токена
    path('api/get_token/', account.GetToken.as_view()),
    # Выход с учетной записи
    path('api/logout/', account.LogoutView.as_view()),
]