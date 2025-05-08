from django.views.generic import ListView, DetailView
from django.shortcuts import render
from viewer.models import Habit, Category, Obstacle


#FUNKCIONALITA
def home(request):
    return render(request, 'home.html')


class HabitsListView(ListView):
    template_name = 'habits.html'
    model = Habit
    context_object_name = 'habits'


class HabitDetailView(DetailView):
    template_name = 'habit.html'
    model = Habit
    context_object_name = 'habit'


class CategoriesListView(ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'categories'


class ObstaclesListView(ListView):
    template_name = 'obstacles.html'
    model = Obstacle
    context_object_name = 'obstacles'
