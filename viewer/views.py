from msilib.schema import ListView
from django.shortcuts import render
from viewer.models import Habit



#FUNKCIONALITA
def home(request):
    return render(request, 'home.html')


class HabitsListView(ListView):# dělám to objektově -  chci seznam = listview
    template_name = 'habits.html'# do jaké temlaty posílám
    model = Habit#z jaké tabulky to vytahuju
    #pozor do tamplate se posilaji data pod nazvem 'object_list', mužu nechat pouze "template_name a model a vpravit přímotepllate {% for habit in 'object_list'%}
    # nebo přidat řádek context_object_name a definovat to zde
    context_object_name = 'habits'

