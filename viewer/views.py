from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Avg
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect

from accounts.models import Profile
from viewer.forms import HabitModelForm, ObstacleModelForm, RewardModelForm, ReviewModelForm, ImageModelForm
from viewer.mixins import StaffRequiredMixin
from viewer.models import Habit, Category, Obstacle, Reward, Review, Image


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


def habit(request, pk):
    if Habit.objects.filter(id=pk).exists():
        habit_ = Habit.objects.get(id=pk)
        if request.method == 'POST':
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

            if Review.objects.filter(habit=habit_, reviewer=Profile.objects.get(user=request.user)).exists():
                user_review = Review.objects.get(habit=habit_, reviewer=Profile.objects.get(user=request.user))
                user_review.rating = rating
                user_review.comment = comment
                user_review.save()
            else:

                Review.objects.create(
                    habit=habit_,
                    reviewer=Profile.objects.get(user=request.user),
                    rating=rating,
                    comment=comment
                )
        rating_avg = habit_.reviews.aggregate(Avg('rating'))['rating__avg']
        rating_count = habit_.reviews.filter(rating__isnull=False).count()

        context = {'habit': habit_,
                   'review_form' : ReviewModelForm,
                   'rating_avg': rating_avg,
                   'rating_count': rating_count}
        return render(request, 'habit.html', context)
    return redirect('habits')


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


class ReviewDeleteView(DeleteView):
    template_name = 'confirm_delete.html'
    model = Review
    success_url = reverse_lazy('habits')








class ImageListView(ListView):
    template_name = 'images.html'
    model = Image
    context_object_name = 'images'


class ImageDetailView(DetailView):
    model = Image
    template_name = 'image.html'



class ImageCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'form_image.html'
    form_class = ImageModelForm
    success_url = reverse_lazy('home')
    permission_required = 'viewer.add_image'


class ImageUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'form_image.html'
    form_class = ImageModelForm
    success_url = reverse_lazy('images')
    model = Image
    permission_required = 'viewer.change_image'


class ImageDeleteView(PermissionRequiredMixin,DeleteView):
    template_name = 'confirm_delete.html'
    model = Image
    success_url = reverse_lazy('images')
    permission_required = 'viewer.delete_image'


