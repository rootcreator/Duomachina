from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser 
from .models import (
    Media, Comment, Rating, 
    Magazine,
    MagazineCategory,
    Category, Tag, Favorite
)
from .serializers import (
    MediaSerializer, CommentSerializer, RatingSerializer, 
    MagazineSerializer, MagazineCategorySerializer
)
from django.db.models import Count, Avg, Sum, Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.db import models
from django.contrib import messages
from .forms import MediaForm, CommentForm, RatingForm, MagazineForm


def home(request):
    """Home page view showing featured content and recent uploads."""
    # Get featured media
    featured_media = Media.objects.filter(
        status='published'
    ).select_related('artist').order_by('-views')[:6]
    
    # Get latest media
    latest_media = Media.objects.filter(
        status='published'
    ).select_related('artist').order_by('-created_at')[:6]
    
    # Get popular categories
    popular_categories = Category.objects.annotate(
        media_count=Count('media', filter=Q(media__status='published'))
    ).filter(media_count__gt=0).order_by('-media_count')[:8]
    
    context = {
        'featured_media': featured_media,
        'latest_media': latest_media,
        'popular_categories': popular_categories,
    }
    
    return render(request, 'media/home.html', context)

def gallery(request):
    """Gallery view showing all published media with enhanced filtering."""
    # Get filter parameters
    media_type = request.GET.get('type')
    artist = request.GET.get('artist')
    sort_by = request.GET.get('sort', '-created_at')  # Default sort by newest
    
    # Start with all published media
    media_list = Media.objects.filter(status='published').select_related('artist')
    
    # Apply filters
    if media_type:
        media_list = media_list.filter(media_type=media_type)
    
    if artist:
        media_list = media_list.filter(artist__username=artist)
    
    # Apply sorting
    valid_sort_fields = {
        'newest': '-created_at',
        'oldest': 'created_at',
        'title_asc': 'title',
        'title_desc': '-title',
        'most_viewed': '-views',
        'most_rated': '-rating_count'
    }
    
    if sort_by in valid_sort_fields:
        media_list = media_list.order_by(valid_sort_fields[sort_by])
    
    # Add annotations for stats
    media_list = media_list.annotate(
        average_rating=Avg('media_ratings__rating'),
        rating_count=Count('media_ratings'),
        comment_count=Count('media_comments')
    )
    
    # Get stats for the hero section
    stats = {
        'total_creators': Media.objects.values('artist').distinct().count(),
        'total_content': Media.objects.filter(status='published').count(),
        'total_views': Media.objects.aggregate(total=Sum('views'))['total'] or 0,
        'avg_rating': Media.objects.annotate(
            avg_rating=Avg('media_ratings__rating')
        ).aggregate(total=Avg('avg_rating'))['total'] or 0
    }
    
    # Get counts for quick stats
    counts = {
        'comics': Media.objects.filter(status='published', media_type='comic').count(),
        'magazines': Magazine.objects.filter(status='published').count(),
        'podcasts': Media.objects.filter(status='published', media_type='podcast').count(),
        'media': Media.objects.filter(status='published').exclude(
            media_type__in=['comic', 'podcast']
        ).count()
    }
    
    # Pagination
    paginator = Paginator(media_list, 12)  # Show 12 items per page
    page = request.GET.get('page')
    media_list = paginator.get_page(page)
    
    # Get unique artists for filter dropdown
    artists = Media.objects.values_list('artist__username', flat=True).distinct()
    
    # Get media types from model choices
    media_types = [
        {'value': type_value, 'label': type_label}
        for type_value, type_label in Media.MEDIA_TYPE_CHOICES
    ]
    
    context = {
        'media_list': media_list,
        'artists': artists,
        'media_types': media_types,
        'selected_artist': artist,
        'selected_type': media_type,
        'selected_sort': sort_by,
        'sort_options': [
            {'value': 'newest', 'label': 'Newest First'},
            {'value': 'oldest', 'label': 'Oldest First'},
            {'value': 'title_asc', 'label': 'Title (A-Z)'},
            {'value': 'title_desc', 'label': 'Title (Z-A)'},
            {'value': 'most_viewed', 'label': 'Most Viewed'},
            {'value': 'most_rated', 'label': 'Most Rated'}
        ],
        'stats': stats,
        'counts': counts
    }
    
    return render(request, 'media/gallery.html', context)

def magazine(request):
    categories = MagazineCategory.objects.all()
    selected_category = request.GET.get('category')
    
    magazines = Magazine.objects.select_related('author', 'category').prefetch_related('tags')
    
    if selected_category:
        magazines = magazines.filter(category__name=selected_category)
    
    context = {
        'categories': categories,
        'magazines': magazines,
        'selected_category': selected_category
    }
    return render(request, 'media/magazine.html', context)

def search(request):
    query = request.GET.get('q', '')
    content_type = request.GET.get('type', 'all')
    
    comics = []
    magazines = []
    podcasts = []
    media = []
    
    if query:
        if content_type in ['all', 'comic']:
            comics = Media.objects.select_related('artist').filter(
                title__icontains=query,
                media_type='comic'
            )
        
        if content_type in ['all', 'magazine']:
            magazines = Magazine.objects.select_related('author', 'category').prefetch_related('tags').filter(
                title__icontains=query
            )
        
        if content_type in ['all', 'podcast']:
            podcasts = Media.objects.select_related('artist').filter(
                title__icontains=query,
                media_type='podcast',
                is_podcast_episode=True
            )
        
        if content_type in ['all', 'media']:
            media = Media.objects.select_related('artist').filter(
                title__icontains=query
            ).exclude(media_type__in=['comic', 'podcast'])  # Exclude comics and podcasts since they're handled separately
    
    context = {
        'query': query,
        'content_type': content_type,
        'comics': comics,
        'magazines': magazines,
        'podcasts': podcasts,
        'media': media,
    }
    return render(request, 'media/search.html', context)


class MediaListCreateView(generics.ListCreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(artist=self.request.user)

class MediaDetailView(generics.RetrieveAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        media = Media.objects.get(id=self.kwargs['media_id'])
        serializer.save(user=self.request.user, media=media)

class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        media = Media.objects.get(id=self.kwargs['media_id'])
        serializer.save(user=self.request.user, media=media)

class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class RatingListView(generics.ListAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

# Magazine Category Views
class MagazineCategoryListView(generics.ListCreateAPIView):
    queryset = MagazineCategory.objects.all()
    serializer_class = MagazineCategorySerializer

# Magazine Views
class MagazineListView(generics.ListCreateAPIView):
    queryset = Magazine.objects.all()
    serializer_class = MagazineSerializer

class MagazineDetailView(generics.RetrieveAPIView):
    queryset = Magazine.objects.all()
    serializer_class = MagazineSerializer



def media_detail(request, slug):
    """Detail view for any media item."""
    media = get_object_or_404(Media, slug=slug, status='published')
    
    # Increment view count
    media.views += 1
    media.save()
    
    # Get comments and ratings
    comments = media.media_comments.select_related('user').order_by('-created_at')
    ratings = media.media_ratings.select_related('user')
    
    # Calculate average rating
    avg_rating = ratings.aggregate(avg=Avg('rating'))['avg'] or 0
    
    # Check if user has rated
    user_rating = None
    if request.user.is_authenticated:
        user_rating = ratings.filter(user=request.user).first()
    
    context = {
        'media': media,
        'comments': comments,
        'ratings': ratings,
        'avg_rating': round(avg_rating, 1),
        'user_rating': user_rating,
    }
    
    return render(request, 'media/media_detail.html', context)

def magazine_detail(request, slug):
    """View for displaying individual magazine details."""
    magazine = get_object_or_404(Magazine, slug=slug)
    context = {
        'magazine': magazine,
        'comments': magazine.magazine_comments.select_related('user').order_by('-created_at'),
        'ratings': magazine.magazine_ratings.select_related('user'),
    }
    return render(request, 'media/magazine_detail.html', context)

@login_required
def create_content(request):
    """View for creating new content."""
    context = {
        'media_types': Media.MEDIA_TYPE_CHOICES,
    }
    return render(request, 'media/create.html', context)

@login_required
def create_media(request):
    """View for creating new media."""
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.artist = request.user
            media.save()
            
            # Handle categories and tags
            categories = request.POST.getlist('categories')
            tags = request.POST.getlist('tags')
            
            if categories:
                media.categories.set(categories)
            
            if tags:
                media.tags.set(tags)
            
            messages.success(request, 'Your media has been created successfully!')
            return redirect(media.get_absolute_url())
    else:
        form = MediaForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
    }
    
    return render(request, 'media/create_media.html', context)

@login_required
def add_comment(request, media_id):
    """Add a comment to a media item."""
    media = get_object_or_404(Media, id=media_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.media = media
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect(media.get_absolute_url())
    
    return redirect(media.get_absolute_url())

@login_required
def delete_comment(request, comment_id):
    """Delete a comment from a media item."""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user is the comment owner or has permission to delete
    if comment.user == request.user or request.user.is_staff:
        media = comment.media
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect(media.get_absolute_url())
    else:
        messages.error(request, 'You do not have permission to delete this comment.')
        return redirect(comment.media.get_absolute_url())

@login_required
def add_rating(request, media_id):
    """Add a rating to a media item."""
    media = get_object_or_404(Media, id=media_id)
    
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            # Check if user has already rated this media
            existing_rating = Rating.objects.filter(user=request.user, media=media).first()
            if existing_rating:
                existing_rating.rating = form.cleaned_data['rating']
                existing_rating.save()
                messages.success(request, 'Rating updated successfully!')
            else:
                rating = form.save(commit=False)
                rating.user = request.user
                rating.media = media
                rating.save()
                messages.success(request, 'Rating added successfully!')
    
    return redirect(media.get_absolute_url())

@login_required
def toggle_favorite(request, media_id):
    """Toggle favorite status of a media item."""
    media = get_object_or_404(Media, id=media_id)
    
    favorite = Favorite.objects.filter(user=request.user, media=media).first()
    if favorite:
        favorite.delete()
        is_favorited = False
        messages.success(request, 'Removed from favorites.')
    else:
        Favorite.objects.create(user=request.user, media=media)
        is_favorited = True
        messages.success(request, 'Added to favorites!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_favorited': is_favorited,
            'favorite_count': Favorite.objects.filter(media=media).count()
        })
    
    return redirect(media.get_absolute_url())

@login_required
def create_magazine(request):
    """View for creating a new magazine."""
    if request.method == 'POST':
        form = MagazineForm(request.POST, request.FILES)
        if form.is_valid():
            magazine = form.save(commit=False)
            magazine.author = request.user
            magazine.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Magazine created successfully!')
            return redirect('media:magazine_detail', slug=magazine.slug)
    else:
        form = MagazineForm()
    
    context = {
        'form': form,
        'title': 'Create Magazine',
        'submit_text': 'Create',
    }
    return render(request, 'media/magazine_form.html', context)

