from rest_framework import serializers
from .models import Account, RecognitionData, Metric, Recommendation

class RecognitionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognitionData
        fields = '__all__'


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognitionData
        fields = '__all__'


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecognitionData
        fields = '__all__'


# ==================================================================================
# АККАУНТЫ
# ==================================================================================


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'is_moderator', 'name', 'lastname', 'fathername']


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