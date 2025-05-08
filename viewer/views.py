from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render

from viewer.forms import HabitModelForm
from viewer.models import Habit, Category, Obstacle, Reward


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

class HabitCreateView(CreateView):
    template_name = 'form.html'
    form_class = HabitModelForm
    success_url = reverse_lazy('habits')

class HabitUpdateView(UpdateView):
    template_name = 'form.html'
    form_class = HabitModelForm
    model = Habit
    success_url = reverse_lazy('habits')

    def form_invalid(self, form):
        print("Formulář není validní.")
        return super().form_invalid(form)

class HabitDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Habit
    success_url = reverse_lazy('habits')







class CategoriesListView(ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'categories'


class ObstaclesListView(ListView):
    template_name = 'obstacles.html'
    model = Obstacle
    context_object_name = 'obstacles'

class ObstacleDetailView(DetailView):
    template_name = 'obstacle.html'
    model = Obstacle
    context_object_name = 'obstacle'

class RewardsListView(ListView):
    template_name = 'rewards.html'
    model = Reward
    context_object_name = 'rewards'


class RewardDetailView(DetailView):
    template_name = 'reward.html'
    model = Reward
    context_object_name = 'reward'
