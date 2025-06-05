from django.contrib import admin
from .models import (
    Category, MagazineCategory, PodcastCategory, Tag,
    Media, Comic, Magazine, Podcast,
    Comment, Rating, Subscription
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(MagazineCategory)
class MagazineCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(PodcastCategory)
class PodcastCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'media_type', 'created_at')
    list_filter = ('media_type', 'created_at', 'categories', 'language')
    search_fields = ('title', 'artist__username', 'description', 'author_name')
    filter_horizontal = ('categories', 'tags')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    def get_fieldsets(self, request, obj=None):
        # Common fields that appear in all forms
        common_fields = (
            (None, {
                'fields': ('title', 'description', 'artist', 'media_type', 'file')
            }),
            ('Categorization', {
                'fields': ('categories', 'tags'),
            }),
        )

        # Media type specific fields
        type_specific_fields = {
            'image': (
                'Image Details',
                {
                    'classes': ('collapse',),
                    'fields': (
                        'image_width', 'image_height', 'image_format',
                        'camera_model', 'exposure_time', 'focal_length',
                        'is_panorama'
                    ),
                }
            ),
            'audio': (
                'Audio Details',
                {
                    'classes': ('collapse',),
                    'fields': (
                        'duration', 'audio_format', 'sample_rate', 'bit_rate',
                        'is_podcast_episode', 'episode_number'
                    ),
                }
            ),
            'video': (
                'Video Details',
                {
                    'classes': ('collapse',),
                    'fields': (
                        'duration', 'video_format', 'video_width', 'video_height',
                        'frame_rate', 'has_subtitles', 'is_series_episode',
                        'video_series_name', 'video_season_number', 'video_episode_number'
                    ),
                }
            ),
            'book': (
                'Book Details',
                {
                    'classes': ('collapse',),
                    'fields': (
                        'author_name', 'publication_date', 'isbn', 'page_count',
                        'language', 'book_publisher', 'edition', 'is_book_series',
                        'book_series_name', 'book_series_number'
                    ),
                }
            ),
            'manuscript': (
                'Manuscript Details',
                {
                    'classes': ('collapse',),
                    'fields': (
                        'author_name', 'manuscript_date', 'manuscript_location',
                        'manuscript_condition', 'restoration_history', 'origin_location',
                        'script_type', 'material', 'page_count', 'language'
                    ),
                }
            ),
        }

        # Timestamps section that appears in all forms
        timestamps = (
            'Timestamps',
            {
                'classes': ('collapse',),
                'fields': ('created_at', 'updated_at'),
            }
        )

        if obj is None:
            # This is an 'add' form - return all fieldsets
            fieldsets = list(common_fields)
            for media_type in type_specific_fields.values():
                fieldsets.append(media_type)
            fieldsets.append(timestamps)
            return fieldsets
        else:
            # This is a 'change' form - return only relevant fieldsets
            fieldsets = list(common_fields)
            if obj.media_type in type_specific_fields:
                fieldsets.append(type_specific_fields[obj.media_type])
            fieldsets.append(timestamps)
            return fieldsets

    def get_list_display(self, request):
        list_display = ['title', 'artist', 'media_type', 'created_at']
        # Add type-specific fields to list_display
        if request.GET.get('media_type') == 'book':
            list_display.extend(['author_name', 'publication_date', 'isbn'])
        elif request.GET.get('media_type') == 'manuscript':
            list_display.extend(['author_name', 'manuscript_date', 'manuscript_location'])
        elif request.GET.get('media_type') == 'video':
            list_display.extend(['duration', 'video_format'])
        elif request.GET.get('media_type') == 'audio':
            list_display.extend(['duration', 'audio_format'])
        elif request.GET.get('media_type') == 'image':
            list_display.extend(['image_format', 'image_width', 'image_height'])
        return list_display

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'issue_number', 'comic_publisher', 'release_date', 'created_at')
    list_filter = ('comic_publisher', 'release_date', 'created_at')
    search_fields = ('title', 'artist__username', 'description', 'comic_publisher')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'release_date'
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'artist', 'issue_number', 'comic_publisher')
        }),
        ('Publication Details', {
            'fields': ('release_date', 'cover_image')
        }),
        ('Timestamps', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at')
        })
    )

@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'issue_number', 'category', 'release_date')
    list_filter = ('category', 'release_date', 'created_at')
    search_fields = ('title', 'author__username', 'description')
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'release_date'
    autocomplete_fields = ['author', 'category']

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'release_date')
    list_filter = ('category', 'release_date', 'created_at')
    search_fields = ('title', 'author__username', 'description')
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'release_date'
    autocomplete_fields = ['author', 'category']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'content_object', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'content')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

    def content_type(self, obj):
        if obj.media:
            return 'Media'
        elif obj.magazine:
            return 'Magazine'
        elif obj.podcast:
            return 'Podcast'
        elif obj.comic:
            return 'Comic'
        return 'Unknown'
    content_type.short_description = 'Content Type'

    def content_object(self, obj):
        return obj.media or obj.magazine or obj.podcast or obj.comic
    content_object.short_description = 'Content'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'content_type', 'content_object', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def content_type(self, obj):
        if obj.media:
            return 'Media'
        elif obj.magazine:
            return 'Magazine'
        elif obj.podcast:
            return 'Podcast'
        elif obj.comic:
            return 'Comic'
        return 'Unknown'
    content_type.short_description = 'Content Type'

    def content_object(self, obj):
        return obj.media or obj.magazine or obj.podcast or obj.comic
    content_object.short_description = 'Content'

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_type', 'content_id', 'subscription_date')
    list_filter = ('content_type', 'subscription_date')
    search_fields = ('user__username',)
    readonly_fields = ('subscription_date',)
    date_hierarchy = 'subscription_date'