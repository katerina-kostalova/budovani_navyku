import os
from datetime import  datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import requests
from django.db.models import Avg
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.models import Profile
from budovani_navyku.settings import DEBUG
from viewer.forms import HabitModelForm, ObstacleModelForm, RewardModelForm, ReviewModelForm, ImageModelForm
from viewer.models import Habit, Category, Obstacle, Reward, Review, Image


#FUNKCIONALITA
def home(request):
    return render(request, 'home.html')






class HabitsListView(ListView):
    template_name = 'habits.html'
    model = Habit
    context_object_name = 'habits'
    paginate_by = 10



class HabitDetailView(DetailView):
    template_name = 'habit.html'
    model = Habit
    context_object_name = 'habit'


def habit(request, pk):
    if Habit.objects.filter(id=pk).exists():
        habit_ = Habit.objects.get(id=pk)
        profile_ = Profile.objects.get(user=request.user)
        if request.method == 'POST':
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')


            if Review.objects.filter(habit=habit_, reviewer=Profile.objects.get(user=request.user)).exists():
                user_review = Review.objects.get(habit=habit_, reviewer=profile_)
                user_review.rating = rating
                user_review.comment = comment
                user_review.save()
            else:

                Review.objects.create(
                    habit=habit_,
                    reviewer=profile_,
                    rating=rating,
                    comment=comment
                )

        rating_avg = habit_.reviews.aggregate(Avg('rating'))['rating__avg']
        rating_count = habit_.reviews.filter(rating__isnull=False).count()

        context = {'habit': habit_,
                   'review_form' : ReviewModelForm,
                   'rating_avg': rating_avg,
                   'rating_count': rating_count,
                    'profile' : profile_ }
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
    paginate_by = 10


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
    paginate_by = 10



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


            #google search api
            url = (f"https://www.googleapis.com/customsearch/v1"
                   f"?key={os.getenv('GOOGLE_API_KEY')}"
                   f"&cx={os.getenv('GOOGLE_CX')}"
                   f"&q={search_string}")
            g_request = requests.get(url)
            if DEBUG:
                print(f"g_request: {g_request}")
            g_json = g_request.json()
            if DEBUG:
                for g_result in g_json['items']:
                    print(g_result['title'])
                    print(f"\t{g_result['link']}")
                    print(f"\t{g_result['displayLink']}")
                    print(f"\t{g_result['snippet']}")




            context = { 'search' : search_string,
                        'habit_name' : habit_name,
                        'habit_description' : habit_description,
                        'category_name' : category_name,
                        'obstacle_name' : obstacle_name,
                        'obstacle_description' : obstacle_description,
                        'reward_name' : reward_name,
                        'reward_description' : reward_description,
                        'g_json' : g_json}

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


def name_day(request):
    month = datetime.today().month
    if month < 10:
        month = f"0{month}"
    day = datetime.today().day
    if day < 10:
        day = f"0{day}"
    url=f"https://svatky.adresa.info/json?date={day}{month}"
    result_request = requests.get(url)
    result_json = result_request.json()
    name = result_json[0]['name']
    context = {'name': name}
    return render(request, 'nameday.html', context)




def weather(request):
    API_KEY = "1638db17866b5132025c3086013f785b"
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}"

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecast1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecast2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecast2 = None, None

        context = {"weather_data1": weather_data1,
                   "daily_forecasts1": daily_forecast1,
                   "weather_data2": weather_data2,
                   "daily_forecasts2": daily_forecast2

        }
        return render(request, "weather.html", context)
    else:
        return render(request, "weather.html")



def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    import datetime

    # Volání aktuálního počasí
    response = requests.get(current_weather_url.format(city, api_key)).json()

    # Bezpečné získání lat/lon, tady se ale teď nevyužívá forecast z One Call API, takže není potřeba
    if response.get('cod') != 200:
        return {"city": city, "error": response.get('message', 'Chyba API')}, []

    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 273.15, 2),
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon'],
    }

    # Volání forecastu (5 dní po 3 hodinách)
    forecast_response = requests.get(forecast_url.format(city, api_key)).json()

    if forecast_response.get('cod') != "200":
        return weather_data, []

    # Forecast poskytuje data po 3 hodinách, z toho vybíráme cca jedno denní (např. po 12:00)
    daily_forecasts = []
    processed_dates = set()

    for item in forecast_response.get('list', []):
        dt_txt = item['dt_txt']  # např. '2025-05-17 12:00:00'
        date = dt_txt.split(' ')[0]

        # Přidáme pouze jeden záznam na den, ideálně ten s 12:00
        time = dt_txt.split(' ')[1]
        if date not in processed_dates and time == "12:00:00":
            daily_forecasts.append({
                "day": datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%A'),
                "min_temp": round(item['main']['temp_min'] - 273.15, 2),
                "max_temp": round(item['main']['temp_max'] - 273.15, 2),
                "description": item['weather'][0]['description'],
                "icon": item['weather'][0]['icon']
            })
            processed_dates.add(date)
            if len(daily_forecasts) == 5:
                break

    return weather_data, daily_forecasts






def acquired_habit(request, pk):
    profile_ = Profile.objects.get(user=request.user)
    habit_ = Habit.objects.get(id=pk)

    if habit_ in profile_.acquired_habit.all():
        profile_.acquired_habit.remove(habit_)
    else:
        profile_.acquired_habit.add(habit_)

    return redirect('habit', pk)


def targeted_habit(request, pk):
    profile_ = Profile.objects.get(user=request.user)
    habit_ = Habit.objects.get(id=pk)

    if habit_ in profile_.targeted_habit.all():
        profile_.targeted_habit.remove(habit_)
    else:
        profile_.targeted_habit.add(habit_)

    return redirect('habit', pk)