from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_artist', 'bio', 'avatar', 'website', 'is_approved')

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'avatar', 'website')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_artist', 'bio', 'avatar', 'website')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ArtistRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_artist', 'bio', 'avatar', 'website', 'is_approved')

    def create(self, validated_data):
        validated_data['is_artist'] = True  # Ensure the user is flagged as an artist
        user = User.objects.create_user(**validated_data)
        return user
