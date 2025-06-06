from django.urls import path

from . import views
from .views import (
    MediaListCreateView, 
    MediaDetailView, 
    CommentCreateView, 
    RatingCreateView,
    MagazineCategoryListView,
    MagazineListView,
    MagazineDetailView,
    CommentListView,
    RatingListView,
)

app_name = 'media'

# Template View URLs
urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('search/', views.search, name='search'),
    
    # Media
    path('media/<slug:slug>/', views.media_detail, name='media_detail'),
    path('media/create/', views.create_media, name='create_media'),
    
    # Magazines
    path('magazines/', views.magazine, name='magazine'),
    path('magazines/<slug:slug>/', views.magazine_detail, name='magazine_detail'),
    path('magazines/create/', views.create_magazine, name='create_magazine'),
    
    # Comments
    path('comment/<int:media_id>/add/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # Ratings
    path('rating/<int:media_id>/add/', views.add_rating, name='add_rating'),
    
    # Favorites
    path('favorite/<int:media_id>/toggle/', views.toggle_favorite, name='toggle_favorite'),
]

# API URLs
api_urlpatterns = [
    path('api/media/', views.MediaListCreateView.as_view(), name='api_media_list'),
    path('api/media/<int:pk>/', views.MediaDetailView.as_view(), name='api_media_detail'),
    path('api/comments/', views.CommentCreateView.as_view(), name='api_comment_create'),
    path('api/ratings/', views.RatingCreateView.as_view(), name='api_rating_create'),
    path('api/comments/<int:pk>/', views.CommentListView.as_view(), name='api_comment_list'),
    path('api/ratings/<int:pk>/', views.RatingListView.as_view(), name='api_rating_list'),
    
    # Magazine API URLs
    path('api/magazine-categories/', MagazineCategoryListView.as_view(), name='api-magazine-category-list'),
    path('api/magazines/', MagazineListView.as_view(), name='api-magazine-list'),
    path('api/magazines/<int:pk>/', MagazineDetailView.as_view(), name='api-magazine-detail'),
]

urlpatterns += api_urlpatterns
