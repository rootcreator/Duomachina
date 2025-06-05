from django.db import models
from django.shortcuts import render
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class MagazineCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Magazine Categories"
    
    def __str__(self):
        return self.name

class PodcastCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Podcast Categories"
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name

class BaseContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('archived', 'Archived')
        ],
        default='draft'
    )
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Media(BaseContent):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('book', 'Book'),
        ('manuscript', 'Manuscript'),
    ]

    # Base fields
    artist = models.ForeignKey(User, related_name='media', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, related_name='media', blank=True)
    tags = models.ManyToManyField(Tag, related_name='media', blank=True)
    file = models.FileField(upload_to='media_files/%Y/%m/%d/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Image specific fields
    image_width = models.PositiveIntegerField(null=True, blank=True, help_text="Width of the image in pixels")
    image_height = models.PositiveIntegerField(null=True, blank=True, help_text="Height of the image in pixels")
    image_format = models.CharField(max_length=10, blank=True, help_text="Format of the image (e.g., JPEG, PNG)")
    camera_model = models.CharField(max_length=100, blank=True, help_text="Camera model used to take the photo")
    exposure_time = models.CharField(max_length=50, blank=True, help_text="Exposure time of the photo")
    focal_length = models.CharField(max_length=50, blank=True, help_text="Focal length used for the photo")
    is_panorama = models.BooleanField(default=False, help_text="Whether this is a panoramic image")

    # Audio specific fields
    duration = models.DurationField(null=True, blank=True, help_text="Duration of the audio/video")
    audio_format = models.CharField(max_length=10, blank=True, help_text="Format of the audio file (e.g., MP3, WAV)")
    sample_rate = models.PositiveIntegerField(null=True, blank=True, help_text="Sample rate in Hz")
    bit_rate = models.PositiveIntegerField(null=True, blank=True, help_text="Bit rate in kbps")
    is_podcast_episode = models.BooleanField(default=False, help_text="Whether this is part of a podcast series")
    episode_number = models.PositiveIntegerField(null=True, blank=True, help_text="Episode number if part of a series")

    # Video specific fields
    video_format = models.CharField(max_length=10, blank=True, help_text="Format of the video file (e.g., MP4, AVI)")
    video_width = models.PositiveIntegerField(null=True, blank=True, help_text="Width of the video in pixels")
    video_height = models.PositiveIntegerField(null=True, blank=True, help_text="Height of the video in pixels")
    frame_rate = models.FloatField(null=True, blank=True, help_text="Frame rate of the video (fps)")
    has_subtitles = models.BooleanField(default=False, help_text="Whether the video has subtitles")
    is_series_episode = models.BooleanField(default=False, help_text="Whether this is part of a video series")
    video_series_name = models.CharField(max_length=255, blank=True, help_text="Name of the series if part of one")
    video_season_number = models.PositiveIntegerField(null=True, blank=True, help_text="Season number if part of a series")
    video_episode_number = models.PositiveIntegerField(null=True, blank=True, help_text="Episode number if part of a series")

    # Book specific fields
    author_name = models.CharField(max_length=255, blank=True, help_text="Author's name for books and manuscripts")
    publication_date = models.DateField(null=True, blank=True, help_text="Publication date for books")
    isbn = models.CharField(max_length=13, blank=True, help_text="ISBN for books")
    page_count = models.PositiveIntegerField(null=True, blank=True, help_text="Number of pages")
    language = models.CharField(max_length=50, blank=True, help_text="Primary language of the content")
    book_publisher = models.CharField(max_length=255, blank=True, help_text="Publisher of the book")
    edition = models.CharField(max_length=50, blank=True, help_text="Edition of the book")
    is_book_series = models.BooleanField(default=False, help_text="Whether this is part of a book series")
    book_series_name = models.CharField(max_length=255, blank=True, help_text="Name of the series if part of one")
    book_series_number = models.PositiveIntegerField(null=True, blank=True, help_text="Book number in the series")

    # Manuscript specific fields
    manuscript_date = models.DateField(null=True, blank=True, help_text="Original date of the manuscript")
    manuscript_location = models.CharField(max_length=255, blank=True, help_text="Physical location of the manuscript")
    manuscript_condition = models.CharField(max_length=100, blank=True, help_text="Current condition of the manuscript")
    restoration_history = models.TextField(blank=True, help_text="History of restoration work")
    origin_location = models.CharField(max_length=255, blank=True, help_text="Original location of the manuscript")
    script_type = models.CharField(max_length=100, blank=True, help_text="Type of script used in the manuscript")
    material = models.CharField(max_length=100, blank=True, help_text="Material of the manuscript (e.g., parchment, paper)")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Media'

    def __str__(self):
        return f'{self.title} by {self.artist.username}'

    def clean(self):
        from django.core.exceptions import ValidationError
        # Validate required fields based on media type
        if self.media_type == 'book':
            if not self.author_name:
                raise ValidationError({'author_name': 'Author name is required for books'})
            if not self.publication_date:
                raise ValidationError({'publication_date': 'Publication date is required for books'})
        elif self.media_type == 'manuscript':
            if not self.author_name:
                raise ValidationError({'author_name': 'Author name is required for manuscripts'})
            if not self.manuscript_date:
                raise ValidationError({'manuscript_date': 'Manuscript date is required'})
            if not self.manuscript_location:
                raise ValidationError({'manuscript_location': 'Manuscript location is required'})
        elif self.media_type == 'video':
            if not self.duration:
                raise ValidationError({'duration': 'Duration is required for videos'})
            if not self.video_format:
                raise ValidationError({'video_format': 'Video format is required'})
        elif self.media_type == 'audio':
            if not self.duration:
                raise ValidationError({'duration': 'Duration is required for audio files'})
            if not self.audio_format:
                raise ValidationError({'audio_format': 'Audio format is required'})
        elif self.media_type == 'image':
            if not self.image_format:
                raise ValidationError({'image_format': 'Image format is required'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('media:media_detail', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('media:media_edit', kwargs={'slug': self.slug})

class Comic(models.Model):
    artist = models.ForeignKey(User, related_name='comics', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    issue_number = models.PositiveIntegerField()
    comic_publisher = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='comic_covers/%Y/%m/%d/', null=True, blank=True)
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('archived', 'Archived')
        ],
        default='draft'
    )
    
    class Meta:
        verbose_name_plural = 'Comics'
        ordering = ['-release_date']

    def __str__(self):
        return f"{self.title} (Issue {self.issue_number})"

class Magazine(BaseContent):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    issue_number = models.PositiveIntegerField()
    release_date = models.DateField()
    tags = models.ManyToManyField(Tag, related_name='magazines', blank=True)
    category = models.ForeignKey(MagazineCategory, related_name='magazines', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, related_name='magazines', on_delete=models.CASCADE)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='magazine_covers/%Y/%m/%d/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('media:magazine_detail', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('media:magazine_edit', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-release_date']
        unique_together = ('title', 'issue_number')

    def __str__(self):
        return f"{self.title} - Issue {self.issue_number}"

class Podcast(BaseContent):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name='podcasts', blank=True)
    audio_file = models.FileField(upload_to='podcasts/%Y/%m/%d/')
    cover_image = models.ImageField(upload_to='podcast_covers/%Y/%m/%d/', null=True, blank=True)
    release_date = models.DateField()
    category = models.ForeignKey(PodcastCategory, related_name='podcasts', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, related_name='podcasts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('media:podcast_detail', kwargs={'slug': self.slug})

    def get_edit_url(self):
        return reverse('media:podcast_edit', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-release_date']

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    media = models.ForeignKey(Media, related_name='media_comments', on_delete=models.CASCADE, null=True, blank=True)
    magazine = models.ForeignKey(Magazine, related_name='magazine_comments', on_delete=models.CASCADE, null=True, blank=True)
    podcast = models.ForeignKey(Podcast, related_name='podcast_comments', on_delete=models.CASCADE, null=True, blank=True)
    comic = models.ForeignKey(Comic, related_name='comic_comments', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'Comment by {self.user.username}'

    class Meta:
        ordering = ['-created_at']

class Rating(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'), 
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    user = models.ForeignKey(User, related_name='user_ratings', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Change related_name to be specific to each content type
    media = models.ForeignKey(Media, related_name='media_ratings', on_delete=models.CASCADE, null=True, blank=True)
    magazine = models.ForeignKey(Magazine, related_name='magazine_ratings', on_delete=models.CASCADE, null=True, blank=True)
    podcast = models.ForeignKey(Podcast, related_name='podcast_ratings', on_delete=models.CASCADE, null=True, blank=True)
    comic = models.ForeignKey(Comic, related_name='comic_ratings', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.rating} stars by {self.user.username}'

class Subscription(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('magazine', 'Magazine'),
        ('podcast', 'Podcast'),
        ('comic', 'Comic'),
    ]

    user = models.ForeignKey(User, related_name='subscriptions', on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    content_id = models.PositiveIntegerField()
    subscription_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'content_type', 'content_id')

    def __str__(self):
        return f"{self.user.username}'s subscription to {self.content_type} #{self.content_id}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    media = models.ForeignKey(Media, on_delete=models.CASCADE, related_name='media_favorites', null=True, blank=True)
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE, related_name='magazine_favorites', null=True, blank=True)
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='podcast_favorites', null=True, blank=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='comic_favorites', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        content = self.media or self.magazine or self.podcast or self.comic
        return f"{self.user.username} favorited {content.title}"
