from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Template URLs
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('register/artist/', views.artist_register_view, name='artist_register'),
    
    # Password Reset URLs
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'),
         name='password_reset_complete'),
    
    # Profile URLs
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),  # Moved this before the username pattern
    path('profile/', views.user_profile_view, name='profile'),
    path('profile/<str:username>/', views.user_profile_view, name='user_profile'),
    path('artist/<str:username>/', views.artist_profile_view, name='artist_profile'),
    
    # API URLs
    path('api/register/', views.RegisterView.as_view(), name='api_register'),
    path('api/register/artist/', views.ArtistRegisterView.as_view(), name='api_artist_register'),
    path('api/profile/', views.UserProfileView.as_view(), name='api_profile'),
    path('api/artist-profile/', views.ArtistProfileView.as_view(), name='api_artist_profile'),
]