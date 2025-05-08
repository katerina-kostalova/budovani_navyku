import re

from django.forms import ModelForm, CharField, TextInput, DateField, NumberInput
from django.core.exceptions import ValidationError
from viewer.models import Habit, Obstacle



class HabitModelForm(ModelForm):

    class Meta:
        model = Habit
        fields = '__all__'


        labels = {
            'categories' : 'Kategorie',
            'name' : 'Název',
            'description' : 'Popis',
            'frequency' : 'Opakování',
            'target_repetitions' : 'Cíl opakování',
            'status' : 'Stav',
            'time_required' : 'Časová náročnost',
            'goal': 'Cíl',
            'start_date' : 'Začátek',
            'rewards' : 'Odměna',
            'obstacles' : 'Překážky',
        }


        help_texts = {
            'obstacles' : 'Vyber si překážku, která ti bude pravděpodobně bránit v budování návyku.',
            'frequency' : 'Jak často budeš činnost opakovat.'
        }

        error_messages = {
            'name' : {
                'required' : 'Tento údaj je povinný.'
            }
        }

    name = CharField(max_length=64,
                     required=True,
                     widget=TextInput(attrs={'class': 'bg-info'}))



    start_date = DateField(required=False,
                           widget=NumberInput(attrs={'type': 'date'}), #na zakladě verze prohlížeče doplnípo fr, deu stylu tyden začina nedele apod
                           label="Začínám dne")


    def __init__(self, *args, **kwargs):#každé položce se přidala třída form control a změní to vzhled
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


    def clean_name(self):
        initial = self.cleaned_data['name']
        return initial.capitalize()

    def clean_target_repetitions(self):
        target_repetitions = self.cleaned_data.get('target_repetitions')
        if target_repetitions is not None:
            if target_repetitions < 21:
                raise ValidationError("Cílový počet opakování musí být alespoň 21, aby vznikl návyk.")
            if target_repetitions > 90:
                raise ValidationError("Cílový počet opakování nesmí být větší než 90, aby to nebylo příliš frustrující.")
        return target_repetitions
'''
    def clean_start_date(self):
        initial = self.cleaned_data['start_date']
        if initial and initial <= datetime.today().date():
            raise ValidationError("Datum začátku nesmí být starší než dnes.")
        return initial

    def clean_description(self):
        # Každá věta bude začínat velkým písmenem
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)
'''


class ObstacleModelForm(ModelForm):

    class Meta:
        model = Obstacle
        fields = '__all__'

        labels = {
            'name' : 'Název',
            'description' : 'Popis',
            'solution' : 'Řešení'
        }

        help_texts = {
            'solution' : 'Dopředu vymysli, jak se jednotlivé překážky překonáš.'
        }

        name = CharField(max_length=64,
                         required=True,
                         widget=TextInput(attrs={'class': 'bg-info'}))

    def __init__(self, *args, **kwargs):#každé položce se přidala třída form control a změní to vzhled
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        initial = self.cleaned_data['name']
        return initial.capitalize()

    def clean_description(self):                                #12.3. 01:47:00
        initial = self.cleaned_data['description']  # Každá věta bude začínat velkým písmenem
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        return '. '.join(sentence.capitalize() for sentence in sentences)

