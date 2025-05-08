



from django.contrib import admin
from django.urls import path

from viewer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), # když za 8000 nebidi mít nic napsáno, odkážu se na home, zavolámi fci ve views "hoeme", tami vykresli tamplate homehtml
    path('habits/', HabitsListView.as_view(), name='habits'),
    path('habit/<int:pk>/', HabitDetailView.as_view(), name='habit'), #potřebuju id konkrétního návyku 8000/habit/id 1/
    path('habit/create/', HabitCreateView.as_view(), name='habit_create'),
    path('habit/update/<int:pk>/', HabitUpdateView.as_view(), name='habit_update'), #musím definovat, které chci updatovat id
    path('habit/delete/<int:pk>/', HabitDeleteView.as_view(), name='habit_delete'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('obstacles/', ObstaclesListView.as_view(), name='obstacles'),
    path('obstacle/<int:pk>/', ObstacleDetailView.as_view(), name='obstacle'),
    path('obstacle/create/', ObstacleCreateView.as_view(), name='obstacle_create'),
    path('obstacle/update/<int:pk>/', ObstacleUpdateView.as_view(), name='obstacle_update'),
    path('obstacle/delete/<int:pk>/', ObstacleDeleteView.as_view(), name='obstacle_delete'),
    path('rewards/', RewardsListView.as_view(), name='rewards'),
    path('reward/<int:pk>/', RewardDetailView.as_view(), name='reward'),

]
