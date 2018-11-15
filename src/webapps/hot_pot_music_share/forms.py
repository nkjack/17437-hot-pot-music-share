from django import forms
from hot_pot_music_share.models import Marker


class MarkerForm(forms.ModelForm):
    class Meta:
        model = Marker
        fields = ('room_name', 'lat', 'lng')






