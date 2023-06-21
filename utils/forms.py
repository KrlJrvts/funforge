import email

from django import forms

from archives.models import User
from .status import Status


# Add game form
class AddGameForm(forms.Form):
    game_name = forms.CharField(label='Game Name')
    price = forms.DecimalField(label='Price')
    year = forms.IntegerField(label='Year')
    stock = forms.IntegerField(label='Stock')
    players_min = forms.IntegerField(label='Minimum Players')
    players_max = forms.IntegerField(label='Maximum Players')
    description = forms.CharField(label='Description', widget=forms.Textarea)
    status = forms.ChoiceField(label='Status', choices=[(s.value, s.name) for s in Status])
    age_rating_id = forms.ChoiceField(label='Age Rating')
    category_id = forms.ChoiceField(label='Category')
    image_id = forms.ImageField(label='Image')
    skill_id = forms.ChoiceField(label='Skill Level')


class RegisterUserForm(forms.Form):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    phone_number = forms.CharField(label='Phone Number')
    zip_code = forms.CharField(label='Zip Code')
    country = forms.CharField(label='Country')
    county = forms.CharField(label='County')
    city = forms.CharField(label='City')
    street = forms.CharField(label='Street')
    house_number = forms.IntegerField(label='House Number')
    apartment_number = forms.IntegerField(label='Apartment Number')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data

    def save(self):
        # Create a new user with the form data
        user = User(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            is_active=True  # Assuming is_active should be set to True for all registered users
        )
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class EditProfileForm(forms.Form):
    pass
    # Add form for edit profile
