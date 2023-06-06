from django import forms
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
