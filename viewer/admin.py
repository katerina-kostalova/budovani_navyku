from django.contrib import admin

from viewer.models import Category, Obstacle, Reward, Habit, Review, Image

admin.site.register(Category)
admin.site.register(Habit)
admin.site.register(Image)
admin.site.register(Obstacle)
admin.site.register(Review)
admin.site.register(Reward)

