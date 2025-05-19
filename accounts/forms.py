from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic

from django.forms import PasswordInput, Textarea, NumberInput,CharField,  DateField

from accounts.models import Profile


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password1', 'password2']


        labels = {
            'username': 'Uživatelské jméno',
            'first_name': 'Jméno',
            'last_name': 'Příjmení',
            'email': 'E-mail',
            'password1' : 'Heslo',
            'password2' : 'Heslo znovu'

        }

    password1 = CharField(
        widget=PasswordInput(attrs={'placeholder': 'Heslo'}),
        label='Heslo'
    )

    password2 = CharField(
        widget=PasswordInput(attrs={'placeholder': 'Heslo znovu'}),
        label='Heslo znovu'
    )

    date_of_birth = DateField(
        widget=NumberInput(attrs={'type': 'date'}),
        label='Datum narození',
        required = False
    )

    biography = CharField(
        widget=Textarea,
        label='Biografie',
        required=False
    )

    phone = CharField(
        label='Telefonní číslo',
        required=False

    )


    @atomic#buˇˇd se uloží oba najednou, nebo vubec, probihaji najednou
    def save(self, commit=True):
        self.instance.is_active = True
        user= super().save(commit)

        date_of_birth = self.cleaned_data.get('date_of_birth')
        biography = self.cleaned_data.get('biography')
        phone = self.cleaned_data.get('phone')
        profile = Profile(
            user=user,
            date_of_birth=date_of_birth,
            biography=biography,
            phone=phone
        )
        if commit:
            profile.save()
        return user
