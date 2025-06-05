from rest_framework import serializers
from .models import (
    Media, Comment, Rating, Category, Tag, 
    Comic, Podcast, Magazine, 
    MagazineCategory, PodcastCategory
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class MagazineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineCategory
        fields = ['id', 'name', 'description']

class PodcastCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PodcastCategory
        fields = ['id', 'name', 'description']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'user_username', 'created_at', 'updated_at', 'media', 'magazine', 'podcast', 'comic']
        read_only_fields = ['user']

class RatingSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'rating', 'user', 'user_username', 'created_at', 'media', 'magazine', 'podcast', 'comic']
        read_only_fields = ['user']

class MediaSerializer(serializers.ModelSerializer):
    artist_username = serializers.CharField(source='artist.username', read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Media
        fields = ['id', 'title', 'description', 'file', 'media_type', 'artist', 'artist_username', 'categories', 'tags', 'created_at']

class ComicSerializer(MediaSerializer):
    issue_number = serializers.IntegerField()
    publisher = serializers.CharField(max_length=255)

    class Meta:
        model = Comic
        fields = ('id', 'artist', 'artist_username', 'title', 'description', 'file', 'media_type', 'categories', 'tags', 'comments', 'ratings', 'created_at', 'issue_number', 'publisher')

class MagazineSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Magazine
        fields = ['id', 'title', 'description', 'issue_number', 'release_date', 'category', 'category_name', 'author', 'author_username', 'content', 'cover_image', 'tags', 'created_at', 'updated_at']

class PodcastSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Podcast
        fields = ['id', 'title', 'description', 'audio_file', 'cover_image', 'release_date', 'category', 'category_name', 'author', 'author_username', 'tags', 'created_at', 'updated_at']



