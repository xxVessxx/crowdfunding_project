import base64

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError

from collects.models import (
    Collect,
    DonationRecord,
    Payment,
)


User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)

    def to_representation(self, value):
        if not value:
            return None
        with open(value.path, 'rb') as image_file:
            return (
                f'data:image/{value.name.split(".")[-1]};base64,'
                + base64.b64encode(image_file.read()).decode()
            )


class UserSerializer(serializers.ModelSerializer):
    avatar = Base64ImageField()

    class Meta():
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'middle_name',
            'avatar',
        )


class UserRegisterSerializer(UserCreateSerializer):
    avatar = Base64ImageField()

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'first_name',
            'last_name',
            'middle_name',
            'avatar',
            'password',
        )

    def create(self, validated_data):
        """Создает нового пользователя."""
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class AvatarSerializer(serializers.ModelSerializer):
    """Сереализатор аватара пользователя."""

    avatar = Base64ImageField(required=True, allow_null=True)

    class Meta:
        model = User
        fields = ('avatar',)

    def update(self, instance, validated_data):
        """Обновление аватара пользователя."""
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance


class CollectSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    occasion_display = serializers.CharField(
        source='get_occasion_display',
        read_only=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Collect
        fields = (
            'id',
            'author',
            'name',
            'occasion',
            'occasion_display',
            'description',
            'target_amount',
            'collected_amount',
            'donors_count',
            'image',
            'end_date',
        )

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        collect = Collect.objects.create(author=user, **validated_data)
        send_mail(
            'Создан групповой сбор',
            f'Ваш сбор "{collect.name}" успешно создан.',
            'from@example.com',
            [user.email],
            fail_silently=True,
        )
        return collect


class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    collect = serializers.PrimaryKeyRelatedField(queryset=Collect.objects.all())

    class Meta:
        model = Payment
        fields = ('id', 'user', 'collect', 'amount', 'date')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        payment = Payment.objects.create(user=user, **validated_data)
        collect_name = payment.collect.name
        author_email = payment.collect.author.email
        send_mail(
            'Поступил платеж',
            (
                f'Пользователь {user.get_full_name_custom()}'
                f'внес сумму {payment.amount} в сбор "{collect_name}".'
            ),
            'from@example.com',
            [payment.collect.author.email],
            fail_silently=True,
        )
        if author_email:
            send_mail(
                'Новый донат в ваш сбор',
                (
                    f'На ваш сбор "{collect_name}" поступил новый донат'
                    f'в размере {payment.amount} от {user.get_full_name_custom()}.'
                ),
                'from@example.com',
                [author_email],
                fail_silently=True,
            )
        return payment


class DonationRecordSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    collect = serializers.PrimaryKeyRelatedField(
        queryset=Collect.objects.all()
    )

    class Meta:
        model = DonationRecord
        fields = (
            'id',
            'user',
            'collect',
            'amount',
            'date',
        )

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        return DonationRecord.objects.create(user=user, **validated_data)
