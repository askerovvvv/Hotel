from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from applications.account.send_mail import send_mail_message

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):  # validate_password ?
        password = attrs.get('password')
        password2 = attrs.pop('password2')  # почему get-Error | pop норм

        if password != password2:
            raise serializers.ValidationError('Пароль не совпадает')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code

        send_mail_message(code, user.email)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такого email не существует')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                raise serializers.ValidationError('Неверный email или password')
            attrs['user'] = user #
            return attrs


class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('date_joined', 'email', 'is_active', 'is_superuser')

