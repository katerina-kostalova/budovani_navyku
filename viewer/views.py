from django.views.generic import ListView
from django.shortcuts import render
from viewer.models import Habit, Category



#FUNKCIONALITA
def home(request):
    return render(request, 'home.html')


class HabitsListView(ListView):
    template_name = 'habits.html'
    model = Habit
    context_object_name = 'habits'


class CategoryListView(ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'categories'
