from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class BookingForm(forms.Form):
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    number_of_guests = forms.IntegerField(min_value=1)

    def __init__(self, *args, room=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        guests = cleaned_data.get('number_of_guests')

        if check_in and check_in < timezone.localdate():
            self.add_error('check_in', 'Check-in date cannot be in the past.')

        if check_in and check_out and check_out <= check_in:
            self.add_error('check_out', 'Check-out date must be after check-in date.')

        if self.room and guests and guests > self.room.capacity:
            self.add_error('number_of_guests', f'This room allows a maximum of {self.room.capacity} guest(s).')

        return cleaned_data
