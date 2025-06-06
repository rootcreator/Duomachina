from django import forms
from .models import Media, Comment, Rating, Magazine

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = [
            'title', 'description', 'file', 'media_type', 'cover_image',
            'categories', 'tags', 'status',
            # Comic fields
            'issue_number', 'comic_publisher', 'comic_series', 'comic_release_date',
            # Image fields
            'image_width', 'image_height', 'image_format', 'camera_model',
            'exposure_time', 'focal_length', 'is_panorama',
            # Audio fields
            'duration', 'audio_format', 'sample_rate', 'bit_rate',
            'is_podcast_episode', 'episode_number',
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
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'comic_release_date': forms.DateInput(attrs={'type': 'date'}),
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'manuscript_date': forms.DateInput(attrs={'type': 'date'}),
            'duration': forms.TimeInput(attrs={'type': 'time'}),
            'restoration_history': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional initially
        for field in self.fields:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        media_type = cleaned_data.get('media_type')

        # Validate required fields based on media type
        if media_type == 'comic':
            required_fields = ['issue_number', 'comic_publisher', 'comic_release_date']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f'This field is required for comics')

        elif media_type == 'image':
            required_fields = ['image_format']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f'This field is required for images')

        elif media_type == 'audio':
            required_fields = ['duration', 'audio_format']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f'This field is required for audio files')

        elif media_type == 'video':
            required_fields = ['duration', 'video_format']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f'This field is required for videos')

        elif media_type == 'book':
            required_fields = ['author_name', 'publication_date']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f'This field is required for books')

        elif media_type == 'manuscript':
            required_fields = ['author_name', 'manuscript_date', 'manuscript_location']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f'This field is required for manuscripts')

        elif media_type == 'podcast':
            required_fields = ['title', 'description', 'issue_number', 'release_date']
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f'This field is required for podcasts')

        return cleaned_data

class CommentForm(forms.ModelForm):
    """Form for adding comments to media items."""
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Write your comment here...'
        })
    )

    class Meta:
        model = Comment
        fields = ['content']

class RatingForm(forms.ModelForm):
    """Form for rating media items."""
    rating = forms.ChoiceField(
        choices=Rating.RATING_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Rating
        fields = ['rating']

class MagazineForm(forms.ModelForm):
    class Meta:
        model = Magazine
        fields = [
            'title', 'description', 'issue_number', 'release_date',
            'tags', 'category', 'content', 'cover_image', 'status'
        ]
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'content': forms.Textarea(attrs={'rows': 10}),
        } 