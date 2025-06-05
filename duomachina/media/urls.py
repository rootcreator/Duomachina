from django.urls import path

from . import views
from .views import (
    MediaListCreateView, 
    MediaDetailView, 
    CommentCreateView, 
    RatingCreateView,
    MagazineCategoryListView,
    PodcastCategoryListView,
    MagazineListView,
    MagazineDetailView,
    PodcastListView,
    PodcastDetailView,
    CommentListView,
    RatingListView,
)

app_name = 'media'

# Template View URLs
urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('comics/', views.comics, name='comics'),
    path('magazine/', views.magazine, name='magazine'),
    path('podcast/', views.podcast, name='podcast'),
    path('search/', views.search, name='search'),
    path('create/', views.create_content, name='create_content'),
    path('create/comic/', views.create_comic, name='create_comic'),
    path('create/magazine/', views.create_magazine, name='create_magazine'),
    path('create/podcast/', views.create_podcast, name='create_podcast'),
    path('create/media/', views.create_media, name='create_media'),
    
    # Detail views
    path('comics/<int:pk>/', views.comic_detail, name='comic_detail'),
    path('media/<int:pk>/', views.media_detail, name='media_detail'),
    path('magazine/<int:pk>/', views.magazine_detail, name='magazine_detail'),
    path('podcast/<int:pk>/', views.podcast_detail, name='podcast_detail'),
]

# API URLs
api_urlpatterns = [
    path('api/media/', MediaListCreateView.as_view(), name='api-media-list'),
    path('api/media/<int:pk>/', MediaDetailView.as_view(), name='api-media-detail'),
    path('api/media/<int:media_id>/comment/', CommentCreateView.as_view(), name='api-comment-create'),
    path('api/media/<int:media_id>/rating/', RatingCreateView.as_view(), name='api-rating-create'),
    path('api/comments/', CommentListView.as_view(), name='api-comment-list'),
    path('api/ratings/', RatingListView.as_view(), name='api-rating-list'),
    
    # Magazine API URLs
    path('api/magazine-categories/', MagazineCategoryListView.as_view(), name='api-magazine-category-list'),
    path('api/magazines/', MagazineListView.as_view(), name='api-magazine-list'),
    path('api/magazines/<int:pk>/', MagazineDetailView.as_view(), name='api-magazine-detail'),
    
    # Podcast API URLs
    path('api/podcast-categories/', PodcastCategoryListView.as_view(), name='api-podcast-category-list'),
    path('api/podcasts/', PodcastListView.as_view(), name='api-podcast-list'),
    path('api/podcasts/<int:pk>/', PodcastDetailView.as_view(), name='api-podcast-detail'),
]

urlpatterns += api_urlpatterns
