from django.contrib import admin

from viewer.models import Category, Obstacle, Reward, Habit, Review

admin.site.register(Category)
admin.site.register(Obstacle)
admin.site.register(Reward)
admin.site.register(Habit)
admin.site.register(Review)
