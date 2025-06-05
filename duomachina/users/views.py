from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Avg, Sum
from rest_framework import status, permissions, generics, exceptions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, UserProfileSerializer, UserSerializer, ArtistRegisterSerializer
from media.models import Media, Magazine, Podcast, Comic, Comment, Rating, Favorite
from store.models import OrderItem

# API Views
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class ArtistRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ArtistRegisterSerializer

class ArtistProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if not user.is_artist:
            raise exceptions.PermissionDenied("You must be an artist to view this profile.")
        return user

# Template Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
            return redirect('home')
        else:
            return render(request, 'auth/login.html', {'form_errors': True})
    
    return render(request, 'auth/login.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterSerializer(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'auth/register.html', {'form': form})
    
    return render(request, 'auth/register.html')

def artist_register_view(request):
    if request.method == 'POST':
        form = ArtistRegisterSerializer(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'auth/artist_register.html', {'form': form})
    
    return render(request, 'auth/artist_register.html')

@login_required
def user_profile_view(request, username=None):
    user = get_object_or_404(User, username=username) if username else request.user
    active_tab = request.GET.get('tab', 'activity')
    content_type = request.GET.get('type', 'all')
    
    context = {
        'user': user,
        'active_tab': active_tab,
        'content_type': content_type,
    }
    
    if active_tab == 'activity':
        # Get user's recent activities (comments, favorites, ratings)
        activities = []
        
        # Get comments for each content type
        media_comments = Comment.objects.filter(user=user, media__isnull=False).select_related('media', 'user')[:5]
        magazine_comments = Comment.objects.filter(user=user, magazine__isnull=False).select_related('magazine', 'user')[:5]
        podcast_comments = Comment.objects.filter(user=user, podcast__isnull=False).select_related('podcast', 'user')[:5]
        comic_comments = Comment.objects.filter(user=user, comic__isnull=False).select_related('comic', 'user')[:5]
        
        # Get favorites for each content type
        media_favorites = Favorite.objects.filter(user=user, media__isnull=False).select_related('media')[:5]
        magazine_favorites = Favorite.objects.filter(user=user, magazine__isnull=False).select_related('magazine')[:5]
        podcast_favorites = Favorite.objects.filter(user=user, podcast__isnull=False).select_related('podcast')[:5]
        comic_favorites = Favorite.objects.filter(user=user, comic__isnull=False).select_related('comic')[:5]
        
        # Get ratings for each content type
        media_ratings = Rating.objects.filter(user=user, media__isnull=False).select_related('media', 'user')[:5]
        magazine_ratings = Rating.objects.filter(user=user, magazine__isnull=False).select_related('magazine', 'user')[:5]
        podcast_ratings = Rating.objects.filter(user=user, podcast__isnull=False).select_related('podcast', 'user')[:5]
        comic_ratings = Rating.objects.filter(user=user, comic__isnull=False).select_related('comic', 'user')[:5]
        
        # Add media comments to activities
        for comment in media_comments:
            activities.append({
                'type': 'comment',
                'description': f'Commented on {comment.media.title}',
                'created_at': comment.created_at,
                'url': comment.media.get_absolute_url()
            })
        
        # Add magazine comments to activities
        for comment in magazine_comments:
            activities.append({
                'type': 'comment',
                'description': f'Commented on magazine {comment.magazine.title}',
                'created_at': comment.created_at,
                'url': comment.magazine.get_absolute_url()
            })
        
        # Add podcast comments to activities
        for comment in podcast_comments:
            activities.append({
                'type': 'comment',
                'description': f'Commented on podcast {comment.podcast.title}',
                'created_at': comment.created_at,
                'url': comment.podcast.get_absolute_url()
            })
        
        # Add comic comments to activities
        for comment in comic_comments:
            activities.append({
                'type': 'comment',
                'description': f'Commented on comic {comment.comic.title}',
                'created_at': comment.created_at,
                'url': comment.comic.get_absolute_url()
            })
        
        # Add media favorites to activities
        for favorite in media_favorites:
            activities.append({
                'type': 'favorite',
                'description': f'Favorited {favorite.media.title}',
                'created_at': favorite.created_at,
                'url': favorite.media.get_absolute_url()
            })
        
        # Add magazine favorites to activities
        for favorite in magazine_favorites:
            activities.append({
                'type': 'favorite',
                'description': f'Favorited magazine {favorite.magazine.title}',
                'created_at': favorite.created_at,
                'url': favorite.magazine.get_absolute_url()
            })
        
        # Add podcast favorites to activities
        for favorite in podcast_favorites:
            activities.append({
                'type': 'favorite',
                'description': f'Favorited podcast {favorite.podcast.title}',
                'created_at': favorite.created_at,
                'url': favorite.podcast.get_absolute_url()
            })
        
        # Add comic favorites to activities
        for favorite in comic_favorites:
            activities.append({
                'type': 'favorite',
                'description': f'Favorited comic {favorite.comic.title}',
                'created_at': favorite.created_at,
                'url': favorite.comic.get_absolute_url()
            })
        
        # Add media ratings to activities
        for rating in media_ratings:
            activities.append({
                'type': 'rating',
                'description': f'Rated {rating.media.title} {rating.rating} stars',
                'created_at': rating.created_at,
                'url': rating.media.get_absolute_url()
            })
        
        # Add magazine ratings to activities
        for rating in magazine_ratings:
            activities.append({
                'type': 'rating',
                'description': f'Rated magazine {rating.magazine.title} {rating.rating} stars',
                'created_at': rating.created_at,
                'url': rating.magazine.get_absolute_url()
            })
        
        # Add podcast ratings to activities
        for rating in podcast_ratings:
            activities.append({
                'type': 'rating',
                'description': f'Rated podcast {rating.podcast.title} {rating.rating} stars',
                'created_at': rating.created_at,
                'url': rating.podcast.get_absolute_url()
            })
        
        # Add comic ratings to activities
        for rating in comic_ratings:
            activities.append({
                'type': 'rating',
                'description': f'Rated comic {rating.comic.title} {rating.rating} stars',
                'created_at': rating.created_at,
                'url': rating.comic.get_absolute_url()
            })
        
        # Sort activities by creation date and get the 10 most recent
        activities.sort(key=lambda x: x['created_at'], reverse=True)
        context['activities'] = activities[:10]
    
    elif active_tab == 'content':
        # Get user's purchased content through orders
        purchased_items = OrderItem.objects.filter(
            order__user=user,
            order__is_paid=True
        ).select_related('product', 'product__artist')
        
        purchased_content = []
        
        for item in purchased_items:
            if item.product.is_media:
                # For media products, get the actual content
                if content_type in ['all', 'comics']:
                    comics = Comic.objects.filter(id=item.product.id)
                    for comic in comics:
                        purchased_content.append({
                            'title': comic.title,
                            'description': comic.description,
                            'thumbnail': comic.cover,
                            'url': comic.get_absolute_url(),
                            'type': 'comic',
                            'purchase_date': item.order.created_at
                        })
                
                if content_type in ['all', 'magazines']:
                    magazines = Magazine.objects.filter(id=item.product.id)
                    for magazine in magazines:
                        purchased_content.append({
                            'title': magazine.title,
                            'description': magazine.description,
                            'thumbnail': magazine.cover,
                            'url': magazine.get_absolute_url(),
                            'type': 'magazine',
                            'purchase_date': item.order.created_at
                        })
                
                if content_type in ['all', 'podcasts']:
                    podcasts = Podcast.objects.filter(id=item.product.id)
                    for podcast in podcasts:
                        purchased_content.append({
                            'title': podcast.title,
                            'description': podcast.description,
                            'thumbnail': podcast.cover,
                            'url': podcast.get_absolute_url(),
                            'type': 'podcast',
                            'purchase_date': item.order.created_at
                        })
                
                if content_type in ['all', 'media']:
                    media = Media.objects.filter(id=item.product.id)
                    for m in media:
                        purchased_content.append({
                            'title': m.title,
                            'description': m.description,
                            'thumbnail': m.thumbnail,
                            'url': m.get_absolute_url(),
                            'type': 'media',
                            'purchase_date': item.order.created_at
                        })
        
        # Sort content by purchase date
        purchased_content.sort(key=lambda x: x['purchase_date'], reverse=True)
        context['purchased_content'] = purchased_content
    
    elif active_tab == 'favorites':
        # Get favorites for each content type
        media_favorites = Favorite.objects.filter(user=user, media__isnull=False).select_related('media')
        magazine_favorites = Favorite.objects.filter(user=user, magazine__isnull=False).select_related('magazine')
        podcast_favorites = Favorite.objects.filter(user=user, podcast__isnull=False).select_related('podcast')
        comic_favorites = Favorite.objects.filter(user=user, comic__isnull=False).select_related('comic')
        
        # Combine all favorites
        favorites = []
        
        for favorite in media_favorites:
            favorites.append({
                'content': favorite.media,
                'content_type': 'media',
                'created_at': favorite.created_at
            })
        
        for favorite in magazine_favorites:
            favorites.append({
                'content': favorite.magazine,
                'content_type': 'magazine',
                'created_at': favorite.created_at
            })
        
        for favorite in podcast_favorites:
            favorites.append({
                'content': favorite.podcast,
                'content_type': 'podcast',
                'created_at': favorite.created_at
            })
        
        for favorite in comic_favorites:
            favorites.append({
                'content': favorite.comic,
                'content_type': 'comic',
                'created_at': favorite.created_at
            })
        
        # Sort favorites by creation date
        favorites.sort(key=lambda x: x['created_at'], reverse=True)
        context['favorites'] = favorites
    
    elif active_tab == 'comments':
        # Get comments for all content types
        media_comments = Comment.objects.filter(user=user, media__isnull=False).select_related('media', 'user')
        magazine_comments = Comment.objects.filter(user=user, magazine__isnull=False).select_related('magazine', 'user')
        podcast_comments = Comment.objects.filter(user=user, podcast__isnull=False).select_related('podcast', 'user')
        comic_comments = Comment.objects.filter(user=user, comic__isnull=False).select_related('comic', 'user')
        
        # Combine all comments
        all_comments = []
        
        for comment in media_comments:
            all_comments.append({
                'text': comment.text,
                'content_title': comment.media.title,
                'content_url': comment.media.get_absolute_url(),
                'created_at': comment.created_at
            })
        
        for comment in magazine_comments:
            all_comments.append({
                'text': comment.text,
                'content_title': comment.magazine.title,
                'content_url': comment.magazine.get_absolute_url(),
                'created_at': comment.created_at
            })
        
        for comment in podcast_comments:
            all_comments.append({
                'text': comment.text,
                'content_title': comment.podcast.title,
                'content_url': comment.podcast.get_absolute_url(),
                'created_at': comment.created_at
            })
        
        for comment in comic_comments:
            all_comments.append({
                'text': comment.text,
                'content_title': comment.comic.title,
                'content_url': comment.comic.get_absolute_url(),
                'created_at': comment.created_at
            })
        
        # Sort comments by creation date
        all_comments.sort(key=lambda x: x['created_at'], reverse=True)
        context['comments'] = all_comments
    
    return render(request, 'profiles/user_profile.html', context)

@login_required
def artist_profile_view(request, username=None):
    user = get_object_or_404(User, username=username) if username else request.user
    if not user.is_artist:
        return redirect('user_profile', username=user.username)
    
    active_tab = request.GET.get('tab', 'content')
    content_type = request.GET.get('type', 'all')
    
    context = {
        'user': user,
        'active_tab': active_tab,
        'content_type': content_type,
    }
    
    if active_tab == 'content':
        contents = []
        if content_type == 'all' or content_type == 'comics':
            contents.extend(Media.objects.filter(artist=user))
        if content_type == 'all' or content_type == 'magazines':
            contents.extend(Magazine.objects.filter(author=user))
        if content_type == 'all' or content_type == 'podcasts':
            contents.extend(Podcast.objects.filter(author=user))
        
        contents.sort(key=lambda x: x.created_at, reverse=True)
        context['contents'] = contents
    
    elif active_tab == 'stats':
        # Calculate total content count
        media_count = Media.objects.filter(artist=user).count()
        magazine_count = Magazine.objects.filter(author=user).count()
        podcast_count = Podcast.objects.filter(author=user).count()
        comic_count = Comic.objects.filter(artist=user).count()
        total_content = media_count + magazine_count + podcast_count + comic_count
        
        # Calculate total views
        media_views = Media.objects.filter(artist=user).aggregate(total=Sum('views'))['total'] or 0
        magazine_views = Magazine.objects.filter(author=user).aggregate(total=Sum('views'))['total'] or 0
        podcast_views = Podcast.objects.filter(author=user).aggregate(total=Sum('views'))['total'] or 0
        comic_views = Comic.objects.filter(artist=user).aggregate(total=Sum('views'))['total'] or 0
        total_views = media_views + magazine_views + podcast_views + comic_views
        
        # Calculate average ratings
        media_ratings = Rating.objects.filter(media__artist=user).aggregate(avg=Avg('rating'))['avg'] or 0
        magazine_ratings = Rating.objects.filter(magazine__author=user).aggregate(avg=Avg('rating'))['avg'] or 0
        podcast_ratings = Rating.objects.filter(podcast__author=user).aggregate(avg=Avg('rating'))['avg'] or 0
        comic_ratings = Rating.objects.filter(comic__artist=user).aggregate(avg=Avg('rating'))['avg'] or 0
        
        # Calculate total number of ratings
        media_rating_count = Rating.objects.filter(media__artist=user).count()
        magazine_rating_count = Rating.objects.filter(magazine__author=user).count()
        podcast_rating_count = Rating.objects.filter(podcast__author=user).count()
        comic_rating_count = Rating.objects.filter(comic__artist=user).count()
        total_ratings = media_rating_count + magazine_rating_count + podcast_rating_count + comic_rating_count
        
        # Calculate average rating across all content types
        if total_ratings > 0:
            avg_rating = (
                (media_ratings * media_rating_count) +
                (magazine_ratings * magazine_rating_count) +
                (podcast_ratings * podcast_rating_count) +
                (comic_ratings * comic_rating_count)
            ) / total_ratings
        else:
            avg_rating = 0
        
        # Calculate total comments
        media_comments = Comment.objects.filter(media__artist=user).count()
        magazine_comments = Comment.objects.filter(magazine__author=user).count()
        podcast_comments = Comment.objects.filter(podcast__author=user).count()
        comic_comments = Comment.objects.filter(comic__artist=user).count()
        total_comments = media_comments + magazine_comments + podcast_comments + comic_comments
        
        stats = {
            'total_content': total_content,
            'total_views': total_views,
            'avg_rating': round(avg_rating, 1),
            'total_ratings': total_ratings,
            'total_comments': total_comments,
            'content_breakdown': {
                'Comics': comic_count,
                'Magazines': magazine_count,
                'Podcasts': podcast_count,
                'Media': media_count
            }
        }
        context['stats'] = stats
    
    elif active_tab == 'dashboard' and request.user == user:
        context.update({
            'recent_activities': get_recent_activities(user),
            'drafts': get_draft_content(user),
        })
    
    return render(request, 'profiles/artist_profile.html', context)

@login_required
def edit_profile_view(request):
    user = request.user
    
    if request.method == 'POST':
        serializer = UserProfileSerializer(user, data=request.POST, files=request.FILES, partial=True)
        if serializer.is_valid():
            serializer.save()
            return redirect('users:profile')
    else:
        serializer = UserProfileSerializer(user)
    
    context = {
        'user': user,
        'form': serializer,
        'errors': serializer.errors if request.method == 'POST' else None
    }
    return render(request, 'profiles/edit_profile.html', context)

# Helper functions
def get_recent_activities(user):
    activities = []
    
    # Get recent comments for each content type
    media_comments = Comment.objects.filter(
        user=user, media__isnull=False
    ).select_related('user', 'media')[:5]
    
    magazine_comments = Comment.objects.filter(
        user=user, magazine__isnull=False
    ).select_related('user', 'magazine')[:5]
    
    podcast_comments = Comment.objects.filter(
        user=user, podcast__isnull=False
    ).select_related('user', 'podcast')[:5]
    
    comic_comments = Comment.objects.filter(
        user=user, comic__isnull=False
    ).select_related('user', 'comic')[:5]
    
    # Get recent ratings for each content type
    media_ratings = Rating.objects.filter(
        user=user, media__isnull=False
    ).select_related('user', 'media')[:5]
    
    magazine_ratings = Rating.objects.filter(
        user=user, magazine__isnull=False
    ).select_related('user', 'magazine')[:5]
    
    podcast_ratings = Rating.objects.filter(
        user=user, podcast__isnull=False
    ).select_related('user', 'podcast')[:5]
    
    comic_ratings = Rating.objects.filter(
        user=user, comic__isnull=False
    ).select_related('user', 'comic')[:5]
    
    # Add media comments to activities
    for comment in media_comments:
        activities.append({
            'type': 'comment',
            'description': f'{comment.user.username} commented on {comment.media.title}',
            'created_at': comment.created_at,
            'url': comment.media.get_absolute_url()
        })
    
    # Add magazine comments to activities
    for comment in magazine_comments:
        activities.append({
            'type': 'comment',
            'description': f'{comment.user.username} commented on magazine {comment.magazine.title}',
            'created_at': comment.created_at,
            'url': comment.magazine.get_absolute_url()
        })
    
    # Add podcast comments to activities
    for comment in podcast_comments:
        activities.append({
            'type': 'comment',
            'description': f'{comment.user.username} commented on podcast {comment.podcast.title}',
            'created_at': comment.created_at,
            'url': comment.podcast.get_absolute_url()
        })
    
    # Add comic comments to activities
    for comment in comic_comments:
        activities.append({
            'type': 'comment',
            'description': f'{comment.user.username} commented on comic {comment.comic.title}',
            'created_at': comment.created_at,
            'url': comment.comic.get_absolute_url()
        })
    
    # Add media ratings to activities
    for rating in media_ratings:
        activities.append({
            'type': 'rating',
            'description': f'{rating.user.username} rated {rating.media.title} {rating.rating} stars',
            'created_at': rating.created_at,
            'url': rating.media.get_absolute_url()
        })
    
    # Add magazine ratings to activities
    for rating in magazine_ratings:
        activities.append({
            'type': 'rating',
            'description': f'{rating.user.username} rated magazine {rating.magazine.title} {rating.rating} stars',
            'created_at': rating.created_at,
            'url': rating.magazine.get_absolute_url()
        })
    
    # Add podcast ratings to activities
    for rating in podcast_ratings:
        activities.append({
            'type': 'rating',
            'description': f'{rating.user.username} rated podcast {rating.podcast.title} {rating.rating} stars',
            'created_at': rating.created_at,
            'url': rating.podcast.get_absolute_url()
        })
    
    # Add comic ratings to activities
    for rating in comic_ratings:
        activities.append({
            'type': 'rating',
            'description': f'{rating.user.username} rated comic {rating.comic.title} {rating.rating} stars',
            'created_at': rating.created_at,
            'url': rating.comic.get_absolute_url()
        })
    
    # Sort activities by creation date and get the 10 most recent
    activities.sort(key=lambda x: x['created_at'], reverse=True)
    return activities[:10]

def get_draft_content(user):
    drafts = []
    # Get drafts for each content type
    media_drafts = Media.objects.filter(artist=user, status='draft').select_related('artist')
    magazine_drafts = Magazine.objects.filter(author=user, status='draft').select_related('author')
    podcast_drafts = Podcast.objects.filter(author=user, status='draft').select_related('author')
    comic_drafts = Comic.objects.filter(artist=user, status='draft').select_related('artist')
    
    # Add all drafts to the list with their type
    for draft in media_drafts:
        drafts.append({
            'type': 'media',
            'title': draft.title,
            'updated_at': draft.updated_at,
            'url': draft.get_absolute_url(),
            'thumbnail': draft.thumbnail.url if draft.thumbnail else None
        })
    
    for draft in magazine_drafts:
        drafts.append({
            'type': 'magazine',
            'title': draft.title,
            'updated_at': draft.updated_at,
            'url': draft.get_absolute_url(),
            'thumbnail': draft.cover.url if draft.cover else None
        })
    
    for draft in podcast_drafts:
        drafts.append({
            'type': 'podcast',
            'title': draft.title,
            'updated_at': draft.updated_at,
            'url': draft.get_absolute_url(),
            'thumbnail': draft.cover.url if draft.cover else None
        })
    
    for draft in comic_drafts:
        drafts.append({
            'type': 'comic',
            'title': draft.title,
            'updated_at': draft.updated_at,
            'url': draft.get_absolute_url(),
            'thumbnail': draft.cover.url if draft.cover else None
        })
    
    # Sort all drafts by update date
    drafts.sort(key=lambda x: x['updated_at'], reverse=True)
    return drafts[:5]
