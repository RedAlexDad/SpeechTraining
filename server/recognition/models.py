from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager


# Пользователь
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_moderator', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")
    username = models.CharField(max_length=255, unique=True, verbose_name="Никнейм")
    password = models.CharField(max_length=255, verbose_name="Пароль")
    is_moderator = models.BooleanField(default=False, verbose_name="Является ли пользователь логопедом?")

    # Necessary fields for django
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    name = models.TextField(verbose_name="Имя")
    lastname = models.TextField(verbose_name="Фамилия")
    fathername = models.TextField(verbose_name="Отчество")

    def str(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.username}"

    class Meta:
        db_table = 'account'
        verbose_name = "Пользователь"


class DataRecognitionAndSynthesis(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name="ID")
    id_synthesis = models.IntegerField(null=True, verbose_name="ID синтеза")
    id_recognition = models.IntegerField(null=True, verbose_name="ID распознавания")
    id_client = models.IntegerField(null=True, verbose_name="ID клиента")
    id_recommendation = models.IntegerField(null=True, verbose_name="ID рекомендации")

    class Meta:
        db_table = 'data_recognition_and_synthesis'
        verbose_name = "Данные распознавания и синтеза речи"


class RecognitionData(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name="ID")
    data_recognition = models.BinaryField(null=True, verbose_name="Запись голоса")
    text_for_check = models.TextField(null=True, verbose_name="Текст для проверки")
    transcription_text = models.TextField(null=True, verbose_name="Текст транскрибации")
    date_recoding = models.DateField(null=True, verbose_name="Дата записи")
    wer = models.FloatField(null=True, verbose_name="WER")
    cer = models.FloatField(null=True, verbose_name="CER")
    mer = models.FloatField(null=True, verbose_name="MER")
    wil = models.FloatField(null=True, verbose_name="WIL")
    iwer = models.FloatField(null=True, verbose_name="IWER")

    class Meta:
        db_table = 'recognition_data'
        verbose_name = "Распознавание речи"


class SynthesisData(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name="ID")
    data_recognition = models.BinaryField(null=True, verbose_name="Синтез речи")
    text_synthesis = models.TextField(null=True, verbose_name="Текст синтеза")
    text_input = models.TextField(null=True, verbose_name="Введенный текст")
    date_synthesis = models.DateField(null=True, verbose_name="Дата синтеза")
    wer = models.FloatField(null=True, verbose_name="WER")

    class Meta:
        db_table = 'synthesis_data'
        verbose_name = "Синтез речи"


class Recommendation(models.Model):
    id = models.AutoField(primary_key=True, serialize=False, verbose_name="ID")
    id_logodedist = models.IntegerField(null=True, verbose_name="ID логопеда")
    recommendation_type = models.TextField(null=True, verbose_name="Тип рекомендации")
    recommendation_text_by_llm = models.TextField(null=True, verbose_name="Текст рекомендации (LLM)")
    recommendation_text_by_logopedist = models.TextField(null=True, verbose_name="Текст рекомендации (логопед)")
    date_recommendation = models.DateField(null=True, verbose_name="Дата рекомендации")

    class Meta:
        db_table = 'recommendation'
        verbose_name = "Рекомендация"
