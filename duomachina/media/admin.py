from django.contrib import admin
from .models import (
    Media, Comment, Rating, Category, Tag,
    Magazine, MagazineCategory
)

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'media_type', 'status', 'created_at', 'views')
    list_filter = ('media_type', 'status', 'created_at')
    search_fields = ('title', 'description', 'artist__username')
    readonly_fields = ('views', 'slug')
    filter_horizontal = ('categories', 'tags')
    
    def get_fieldsets(self, request, obj=None):
        common_fields = (
            'title', 'description', 'artist', 'file', 'cover_image',
            'categories', 'tags', 'status', 'views', 'slug'
        )
        
        if obj is None:
            return [(None, {'fields': common_fields})]
        
        fieldsets = [(None, {'fields': common_fields})]
        
        if obj.media_type == 'comic':
            fieldsets.append(('Comic Details', {
                'fields': (
                    'issue_number', 'comic_publisher', 'comic_series',
                    'comic_release_date'
                ),
            }))
        elif obj.media_type == 'image':
            fieldsets.append(('Image Details', {
                'fields': (
                    'image_width', 'image_height', 'image_format',
                    'camera_model', 'exposure_time', 'focal_length',
                    'is_panorama'
                ),
            }))
        elif obj.media_type == 'audio':
            fieldsets.append(('Audio Details', {
                'fields': (
                    'duration', 'audio_format', 'sample_rate', 'bit_rate',
                    'is_podcast_episode', 'episode_number'
                ),
            }))
        elif obj.media_type == 'podcast':
            fieldsets.append(('Podcast Details', {
                'fields': (
                    'duration', 'audio_format', 'sample_rate', 'bit_rate',
                    'is_podcast_episode', 'episode_number', 'podcast_series_name',
                    'podcast_season_number', 'podcast_category', 'podcast_release_date'
                ),
            }))
        elif obj.media_type == 'video':
            fieldsets.append(('Video Details', {
                'fields': (
                    'video_format', 'video_width', 'video_height',
                    'frame_rate', 'has_subtitles', 'is_series_episode',
                    'video_series_name', 'video_season_number',
                    'video_episode_number'
                ),
            }))
        elif obj.media_type == 'book':
            fieldsets.append(('Book Details', {
                'fields': (
                    'author_name', 'publication_date', 'isbn', 'page_count',
                    'language', 'book_publisher', 'edition', 'is_book_series',
                    'book_series_name', 'book_series_number'
                ),
            }))
        elif obj.media_type == 'manuscript':
            fieldsets.append(('Manuscript Details', {
                'fields': (
                    'manuscript_date', 'manuscript_location',
                    'manuscript_condition', 'restoration_history',
                    'origin_location', 'script_type', 'material'
                ),
            }))
        
        return fieldsets

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at', 'views')
    list_filter = ('status', 'created_at', 'category')
    search_fields = ('title', 'description', 'author__username')
    readonly_fields = ('views', 'slug')
    filter_horizontal = ('tags',)

@admin.register(MagazineCategory)
class MagazineCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'description')