from rest_framework import serializers
from .models import Account, DataRecognitionAndSynthesis, RecognitionData, Recommendation, SynthesisData, Text


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'


class RecognitionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognitionData
        fields = '__all__'


class DataRecognitionAndSynthesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRecognitionAndSynthesis
        fields = '__all__'


class SynthesisDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynthesisData
        fields = '__all__'


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'


# ==================================================================================
# АККАУНТЫ
# ==================================================================================


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'is_moderator', 'name', 'lastname', 'fathername']

    def update(self, instance, validated_data):
        # Проверяем, предоставлен ли пароль в данных запроса
        if 'password' in validated_data:
            # Если пароль предоставлен, устанавливаем его
            instance.set_password(validated_data['password'])

        # Обновляем остальные поля
        instance.username = validated_data.get('username', instance.username)
        instance.is_moderator = validated_data.get('is_moderator', instance.is_moderator)
        instance.name = validated_data.get('name', instance.name)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.fathername = validated_data.get('fathername', instance.fathername)
        instance.save()

        return instance


class AccountSerializerInfo(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'is_moderator']


# Для аутенфикации, авторизации и регистрации
class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'is_moderator', 'name', 'lastname', 'fathername']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password is not None:
            instance.set_password(password)
        else:
            # Если пароль не предоставлен в запросе, сохраняем текущий пароль
            validated_data['password'] = instance.password

        instance.is_moderator = validated_data.get('is_moderator', instance.is_moderator)
        instance.save()
        return instance


class AccountAuthorizationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
