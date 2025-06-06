from rest_framework import serializers
from .models import (
    Media, Comment, Rating, Category, Tag, 
    Magazine, MagazineCategory
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class MagazineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MagazineCategory
        fields = ['id', 'name', 'description']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')

class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_name', 'media', 'magazine',
                 'text', 'created_at', 'updated_at', 'parent']
        read_only_fields = ['user']

class RatingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'user_name', 'media', 'magazine',
                 'rating', 'created_at']
        read_only_fields = ['user']

class MediaSerializer(serializers.ModelSerializer):
    artist_name = serializers.CharField(source='artist.username', read_only=True)
    categories = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Media
        fields = [
            'id', 'title', 'description', 'artist', 'artist_name', 'categories', 'tags',
            'file', 'media_type', 'cover_image', 'created_at', 'updated_at', 'views',
            'status', 'slug',
            # Comic fields
            'issue_number', 'comic_publisher', 'comic_series', 'comic_release_date',
            # Image fields
            'image_width', 'image_height', 'image_format', 'camera_model',
            'exposure_time', 'focal_length', 'is_panorama',
            # Audio and Podcast fields
            'duration', 'audio_format', 'sample_rate', 'bit_rate',
            'is_podcast_episode', 'episode_number', 'podcast_series_name',
            'podcast_season_number', 'podcast_category', 'podcast_release_date',
            # Video fields
            'video_format', 'video_width', 'video_height', 'frame_rate',
            'has_subtitles', 'is_series_episode', 'video_series_name',
            'video_season_number', 'video_episode_number',
            # Book fields
            'author_name', 'publication_date', 'isbn', 'page_count',
            'language', 'book_publisher', 'edition', 'is_book_series',
            'book_series_name', 'book_series_number',
            # Manuscript fields
            'manuscript_date', 'manuscript_location', 'manuscript_condition',
            'restoration_history', 'origin_location', 'script_type', 'material'
        ]
        read_only_fields = ['views', 'slug']

class MagazineSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Magazine
        fields = ['id', 'title', 'description', 'issue_number', 'release_date',
                 'tags', 'category', 'category_name', 'author', 'author_name',
                 'content', 'cover_image', 'created_at', 'updated_at', 'views',
                 'status', 'slug']
        read_only_fields = ['views', 'slug']



