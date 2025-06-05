from django.shortcuts import render, get_object_or_404
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser 
from .models import (
    Media, Comment, Rating, 
    Magazine, Comic, Podcast,
    MagazineCategory, PodcastCategory
)
from .serializers import (
    MediaSerializer, CommentSerializer, RatingSerializer, 
    ComicSerializer, MagazineSerializer, PodcastSerializer,
    MagazineCategorySerializer, PodcastCategorySerializer
)
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect


def home(request):
    """Home page view showing featured content and recent uploads."""
    context = {
        'featured_media': Media.objects.filter(status='published').order_by('-views')[:6],
        'latest_comics': Comic.objects.order_by('-created_at')[:4],
        'latest_magazines': Magazine.objects.order_by('-created_at')[:4],
        'latest_podcasts': Podcast.objects.order_by('-created_at')[:4],
    }
    return render(request, 'media/home.html', context)

def gallery(request):
    comics = Comic.objects.select_related('artist').all()
    magazines = Magazine.objects.select_related('author', 'category').prefetch_related('tags').all()
    podcasts = Podcast.objects.select_related('author', 'category').prefetch_related('tags').all()
    media = Media.objects.select_related('artist').all()

    context = {
        'comics': comics,
        'magazines': magazines,
        'podcasts': podcasts,
        'media': media,
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

def podcast(request):
    categories = PodcastCategory.objects.all()
    selected_category = request.GET.get('category')
    
    podcasts = Podcast.objects.select_related('author', 'category').prefetch_related('tags')
    
    if selected_category:
        podcasts = podcasts.filter(category__name=selected_category)
    
    context = {
        'categories': categories,
        'podcasts': podcasts,
        'selected_category': selected_category
    }
    return render(request, 'media/podcast.html', context)

def search(request):
    query = request.GET.get('q', '')
    content_type = request.GET.get('type', 'all')
    
    comics = []
    magazines = []
    podcasts = []
    media = []
    
    if query:
        if content_type in ['all', 'comic']:
            comics = Comic.objects.select_related('artist').filter(
                title__icontains=query
            )
        
        if content_type in ['all', 'magazine']:
            magazines = Magazine.objects.select_related('author', 'category').prefetch_related('tags').filter(
                title__icontains=query
            )
        
        if content_type in ['all', 'podcast']:
            podcasts = Podcast.objects.select_related('author', 'category').prefetch_related('tags').filter(
                title__icontains=query
            )
        
        if content_type in ['all', 'media']:
            media = Media.objects.select_related('artist').filter(
                title__icontains=query
            )
    
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

# Podcast Category Views
class PodcastCategoryListView(generics.ListCreateAPIView):
    queryset = PodcastCategory.objects.all()
    serializer_class = PodcastCategorySerializer

# Magazine Views
class MagazineListView(generics.ListCreateAPIView):
    queryset = Magazine.objects.all()
    serializer_class = MagazineSerializer

class MagazineDetailView(generics.RetrieveAPIView):
    queryset = Magazine.objects.all()
    serializer_class = MagazineSerializer

# Podcast Views
class PodcastListView(generics.ListCreateAPIView):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

class PodcastDetailView(generics.RetrieveAPIView):
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

def comics(request):
    """View for displaying comics with optional filtering."""
    comics = Comic.objects.select_related('artist').order_by('-release_date')
    
    # Get filter parameters
    publisher = request.GET.get('publisher')
    artist = request.GET.get('artist')
    
    # Apply filters
    if publisher:
        comics = comics.filter(comic_publisher__iexact=publisher)
    if artist:
        comics = comics.filter(artist__username=artist)
    
    # Get unique publishers for filter dropdown
    publishers = Comic.objects.values_list('comic_publisher', flat=True).distinct()
    
    context = {
        'comics': comics,
        'publishers': publishers,
        'selected_publisher': publisher,
        'selected_artist': artist,
    }
    return render(request, 'media/comics.html', context)

def comic_detail(request, pk):
    """View for displaying individual comic details."""
    comic = get_object_or_404(Comic, pk=pk)
    context = {
        'comic': comic,
        'comments': comic.comic_comments.select_related('user').order_by('-created_at'),
        'ratings': comic.comic_ratings.select_related('user'),
    }
    return render(request, 'media/comic_detail.html', context)

def media_detail(request, pk):
    """View for displaying individual media details."""
    media = get_object_or_404(Media, pk=pk)
    context = {
        'media': media,
        'comments': media.media_comments.select_related('user').order_by('-created_at'),
        'ratings': media.media_ratings.select_related('user'),
    }
    return render(request, 'media/media_detail.html', context)

def magazine_detail(request, pk):
    """View for displaying individual magazine details."""
    magazine = get_object_or_404(Magazine, pk=pk)
    context = {
        'magazine': magazine,
        'comments': magazine.magazine_comments.select_related('user').order_by('-created_at'),
        'ratings': magazine.magazine_ratings.select_related('user'),
    }
    return render(request, 'media/magazine_detail.html', context)

def podcast_detail(request, pk):
    """View for displaying individual podcast details."""
    podcast = get_object_or_404(Podcast, pk=pk)
    context = {
        'podcast': podcast,
        'comments': podcast.podcast_comments.select_related('user').order_by('-created_at'),
        'ratings': podcast.podcast_ratings.select_related('user'),
    }
    return render(request, 'media/podcast_detail.html', context)

@login_required
def create_content(request):
    """View for creating new content."""
    if not request.user.is_artist:
        return HttpResponseRedirect(reverse('home'))
    
    context = {
        'content_types': [
            {'id': 'comic', 'name': 'Comic'},
            {'id': 'magazine', 'name': 'Magazine'},
            {'id': 'podcast', 'name': 'Podcast'},
            {'id': 'media', 'name': 'Media'}
        ]
    }
    return render(request, 'media/create_content.html', context)

@login_required
def create_comic(request):
    """View for creating a new comic."""
    if not request.user.is_artist:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'POST':
        # Handle form submission
        pass
    
    context = {
        'form': None  # We'll add the form later
    }
    return render(request, 'media/create_comic.html', context)

@login_required
def create_magazine(request):
    """View for creating a new magazine."""
    if not request.user.is_artist:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'POST':
        # Handle form submission
        pass
    
    context = {
        'form': None  # We'll add the form later
    }
    return render(request, 'media/create_magazine.html', context)

@login_required
def create_podcast(request):
    """View for creating a new podcast."""
    if not request.user.is_artist:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'POST':
        # Handle form submission
        pass
    
    context = {
        'form': None  # We'll add the form later
    }
    return render(request, 'media/create_podcast.html', context)

@login_required
def create_media(request):
    """View for creating new media."""
    if not request.user.is_artist:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'POST':
        # Handle form submission
        pass
    
    context = {
        'form': None  # We'll add the form later
    }
    return render(request, 'media/create_media.html', context)

