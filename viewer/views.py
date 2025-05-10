from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render

from viewer.forms import HabitModelForm, ObstacleModelForm, RewardModelForm
from viewer.mixins import StaffRequiredMixin
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

class HabitCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = HabitModelForm
    success_url = reverse_lazy('habits')
    permission_required = 'viewer.add_habit'

class HabitUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = HabitModelForm
    model = Habit
    success_url = reverse_lazy('habits')
    permission_required = 'viewer.change_habit'

    def form_invalid(self, form):
        print("Formulář není validní.")
        return super().form_invalid(form)

class HabitDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Habit
    success_url = reverse_lazy('habits')
    permission_required = 'viewer.delete_habit'







class CategoriesListView(ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    template_name = 'category.html'
    model = Category
    context_object_name = 'category'








class ObstaclesListView(ListView):
    template_name = 'obstacles.html'
    model = Obstacle
    context_object_name = 'obstacles'

class ObstacleDetailView(DetailView):
    template_name = 'obstacle.html'
    model = Obstacle
    context_object_name = 'obstacle'


class ObstacleCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = ObstacleModelForm
    success_url = reverse_lazy('obstacles')
    permission_required = 'viewer.add_obstacle'

    def form_invalid(self, form):
        print("Formulář 'ObstacleModelForm' není validní.")
        return super().form_invalid(form)

class ObstacleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = ObstacleModelForm
    model = Obstacle
    success_url = reverse_lazy('obstacles')
    permission_required = 'viewer.change_obstacle'

    def form_invalid(self, form):
        print("Formulář 'ObstacleModelForm' není validní.")
        return super().form_invalid(form)

class ObstacleDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Obstacle
    success_url = reverse_lazy('obstacles')
    permission_required = 'viewer.delete_obstacle'










class RewardsListView(ListView):
    template_name = 'rewards.html'
    model = Reward
    context_object_name = 'rewards'


class RewardDetailView(DetailView):
    template_name = 'reward.html'
    model = Reward
    context_object_name = 'reward'


class RewardCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = RewardModelForm
    success_url = reverse_lazy('rewards')

    def form_invalid(self, form):
        print("Formulář 'RewardModelForm' není validní.")
        return super().form_invalid(form)
        permission_required = 'viewer.add_reward'


class RewardUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form.html'
    form_class = RewardModelForm
    model = Reward
    success_url = reverse_lazy('rewards')
    permission_required = 'viewer.change_reward'



class RewardDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'confirm_delete.html'
    model = Reward
    success_url = reverse_lazy('rewards')
    permission_required = 'viewer.delete_reward'



def search(request):
    if request.method == 'POST':
        search_string = request.POST.get('search')
        if search_string:
            habit_name = Habit.objects.filter(name__icontains=search_string)
            habit_description = Habit.objects.filter(description__icontains=search_string)
            category_name = Category.objects.filter(name__icontains=search_string)
            obstacle_name = Obstacle.objects.filter(name__icontains=search_string)
            obstacle_description = Obstacle.objects.filter(description__icontains=search_string)
            reward_name = Reward.objects.filter(name__icontains=search_string)
            reward_description = Reward.objects.filter(description__icontains=search_string)


            context = { 'search' : search_string,
                        'habit_name' : habit_name,
                        'habit_description' : habit_description,
                        'category_name' : category_name,
                        'obstacle_name' : obstacle_name,
                        'obstacle_description' : obstacle_description,
                        'reward_name' : reward_name,
                        'reward_description' : reward_description,}

        return render(request, 'search.html', context)
    return render(request, 'home.html')





def habit_filter(request):
    if request.method == 'POST': #pokud uživatel něco odesal,
        filter_category = request.POST.get('filter-category').strip()
        filter_name = request.POST.get('filter-name').strip()
        filter_obstacle = request.POST.get('filter-obstacle').strip()
        filter_reward = request.POST.get('filter-reward').strip()
        filtered_habits = Habit.objects.all()
        if filter_category:
            filtered_habits = filtered_habits.filter(categories__name__icontains=filter_category)
        if filter_name:
            filtered_habits = filtered_habits.filter(name__icontains=filter_name)
        if filter_obstacle:
            filtered_habits = filtered_habits.filter(obstacles__name__icontains=filter_obstacle)
        if filter_reward:
            filtered_habits = filtered_habits.filter(rewards__name__icontains=filter_reward)


        context = { 'habits' : filtered_habits}
        return render(request, 'habits.html', context)
    return render(request, 'home.html') #když nic nepošleme, vrátíme se na home



