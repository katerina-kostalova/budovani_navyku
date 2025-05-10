from django.db.models import (Model, CharField, TextField, DateField, DateTimeField, ForeignKey, ImageField,
                              IntegerField, SET_NULL, BooleanField, ManyToManyField, CASCADE)

from django.contrib.auth.models import User

from accounts.models import Profile


#from accounts.models import Profile










class Category(Model):
    name = CharField(max_length=32, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __repr__(self):
        return f'Category(name=({self.name})'

    def __str__(self):
        return self.name






class Obstacle(Model):
    name = CharField(max_length=1500, null=False, blank=False, unique=True)
    description = TextField(blank=True, null=True)
    solution = TextField(max_length=2000, null=False, blank=False,default="zatím žádné řešení" )
    created_at = DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f'Obstacle(name=({self.name})'

    def __str__(self):
        return self.name





class Reward(Model):
    name = CharField(max_length=200, null=False, blank=False, unique=True)
    description = TextField(max_length=2000, blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f'Reward(name=({self.name})'

    def __str__(self):
        return self.name





class Habit(Model):

    STATUS_CHOICES = (
        ('not_started', 'Nezahájeno'),
        ('in_progress', 'V procesu'),
        ('completed', 'Splněno'),
    )

    FREQUENCY_CHOICES = (
        ('once_a_week', 'jednou týdně'),
        ('twice_a_week', 'dvakrát týdně'),
        ('three_times_a_week', 'třikrát týdně'),
        ('four_times_a_week', 'čtyřikrát týdně'),
        ('five_times_a_week','pětkrát týdně'),
        ('times_a_week','šestkrát týdně'),
        ('everyday' , 'každý den'),
        ('once_a_month', 'jednou měsíčně')

    )
    categories = ManyToManyField(Category, max_length=32, blank=True, related_name='habits')
    name = CharField(max_length=32, null=False, blank=False, unique=True)
    obstacles = ManyToManyField(Obstacle, blank=True, related_name='obstacles')
    rewards = ManyToManyField(Reward, blank=True, related_name='rewards')
    goal = TextField(max_length=100, blank =True, null=True)
    frequency = CharField(max_length=50, choices=FREQUENCY_CHOICES, default='once_a_week')
    target_repetitions = IntegerField(default=21)
    start_date = DateField(blank=True, null=True)
    status = CharField(max_length=32, choices=STATUS_CHOICES, default='not_started')
    created_at = DateTimeField(auto_now_add=True, null=True)
    updated_at = DateTimeField(auto_now=True)
    description = TextField(max_length=5000, null=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f'Habit(name=({self.name})'

    def __str__(self):
        return self.name





class Review(Model):
    habit = ForeignKey(Habit, on_delete=CASCADE, null=False, blank=False, related_name='reviews')
    reviewer = ForeignKey(Profile, on_delete=SET_NULL, null=True, blank=False, related_name='reviews')
    rating = IntegerField(null=True, blank=True)
    comment = TextField(null=True,blank=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __repr__(self):
        return (f"Review(habit={self.habit}, "
                f"reviewer={self.reviewer}, "
                f"rating={self.rating}, "
                f"comment={self.comment[:100]} "
                )

    def __str__(self):
        return f"{self.reviewer}: {self.habit}({self.rating})"

'''



class Image(Model):
    image = ImageField(upload_to='images/', default=None, null=False, blank=False)
    habit = ForeignKey('Habit', on_delete=SET_NULL, null=True, blank=True, related_name='images')
    description = TextField(blank=True, null=True)

    def __repr__(self):
        return f"Image(name=({self.image})"

    def __str__(self):
        return f"Image:{self.image}"
'''
