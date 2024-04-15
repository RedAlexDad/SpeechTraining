# urls.py для account
from django.urls import path
from account import account

urlpatterns = [
    # Список аккаунтов
    path(r'users/', account.AccountGET.as_view()),
    # Обновление аккаунта
    path(r'users/<int:pk>/update/', account.AccountPUT.as_view()),
    # Удаление аккаунта
    path(r'users/<int:pk>/delete/', account.AccountDELETE.as_view()),

    # Регистрация
    path('register/', account.RegisterView.as_view()),
    # Аутентификация
    path('authentication/', account.LoginView.as_view()),
    # Получение токена
    path('get_token/', account.GetToken.as_view()),
    # Выход с учетной записи
    path('logout/', account.LogoutView.as_view()),
]
