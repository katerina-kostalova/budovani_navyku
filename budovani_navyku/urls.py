from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import SubmittableLoginView, user_logout, SignUpView
from django.urls import path, include

from budovani_navyku import settings
from viewer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), # když za 8000 nebidi mít nic napsáno, odkážu se na home, zavolámi fci ve views "hoeme", tami vykresli tamplate homehtml
    path('habits/', HabitsListView.as_view(), name='habits'),
    #path('habit/<int:pk>/', HabitDetailView.as_view(), name='habit'), #potřebuju id konkrétního návyku 8000/habit/id 1/
    path('habit/<int:pk>/', habit, name='habit'),
    path('habit/create/', HabitCreateView.as_view(), name='habit_create'),
    path('habit/update/<int:pk>/', HabitUpdateView.as_view(), name='habit_update'), #musím definovat, které chci updatovat id
    path('habit/delete/<int:pk>/', HabitDeleteView.as_view(), name='habit_delete'),
    path('habit/filter/', habit_filter, name='habit_filter'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category'),
    path('obstacles/', ObstaclesListView.as_view(), name='obstacles'),
    path('obstacle/<int:pk>/', ObstacleDetailView.as_view(), name='obstacle'),
    path('obstacle/create/', ObstacleCreateView.as_view(), name='obstacle_create'),
    path('obstacle/update/<int:pk>/', ObstacleUpdateView.as_view(), name='obstacle_update'),
    path('obstacle/delete/<int:pk>/', ObstacleDeleteView.as_view(), name='obstacle_delete'),
    path('rewards/', RewardsListView.as_view(), name='rewards'),
    path('reward/<int:pk>/', RewardDetailView.as_view(), name='reward'),
    path('reward/create/', RewardCreateView.as_view(), name='reward_create'),
    path('reward/update/<int:pk>/', RewardUpdateView.as_view(), name='reward_update'),
    path('reward/delete/<int:pk>/', RewardDeleteView.as_view(), name='reward_delete'),
    path('images/', ImageListView.as_view(), name='images'),
    path('image/<int:pk>/', ImageDetailView.as_view(), name='image'),
    path('image/create/', ImageCreateView.as_view(), name='image_create'),
    path('image/update/<int:pk>/', ImageUpdateView.as_view(), name='image_update'),
    path('image/delete/<int:pk>/', ImageDeleteView.as_view(), name='image_delete'),


    path('search/', search, name='search'),

    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    #ostatní defaultní cesty, předefinované dábat před tohle
    path('accounts/', include('django.contrib.auth.urls')),
    path('review/delete/<int:pk>/', ReviewDeleteView.as_view(), name='review_delete'),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    #API
    path('nameday/', name_day, name='nameday'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
