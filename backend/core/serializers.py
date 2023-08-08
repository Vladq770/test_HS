from rest_framework import serializers

from .models import User


class UserSerializerSimple(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'invite_code')


class UserSerializer(serializers.ModelSerializer):
    referrer = UserSerializerSimple(read_only=True)

    class Meta:
        model = User
        fields = '__all__'
