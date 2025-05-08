from django.shortcuts import render

from viewer.models import Habit




def home(request):
    return render(request, 'home.html')
#FUNKCIONALITA
def habits(request):
    habits_ = Habit.objects.all() # vytahnu si z databaze všechny filmy
    context = {'habits': habits_} #potřebuju do te templaty poslat data, nazev proměnné 'habits' : tohle je obsa=) habits_
    return render(request=request,#potřebuju poslat request přišel mi od uživatele požadavek, já ho zpracuju a pošlu ho zpátky
                  template_name='habits.html', # tamplate ktera se mi použije pro to zobrazení
                  context=context)#potřebuju data pro to zobrazení

#1.řádek fce vytahne z databaze všechny filmy=)
#2. =) vloží je do nějakého slovníku balíku
#3. =) tím render se pošle do té templaty

