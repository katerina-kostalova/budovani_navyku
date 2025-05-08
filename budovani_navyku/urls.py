



from django.contrib import admin
from django.urls import path

from viewer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'), # když za 8000 nebidi mít nic napsáno, odkážu se na home, zavolámi fci ve views "hoeme", tami vykresli tamplate homehtml
    path('habits/', HabitsListView.as_view(), name='habits'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('habit/<int:pk>/', HabitDetailView.as_view(), name='habit'), #potřebuju id konkrétního návyku 8000/habit/id 1/
    path('obstacles/', ObstaclesListView.as_view(), name='obstacles'),

]
