from django import forms
from django.core.validators import RegexValidator, EmailValidator

from hot_pot.models import *


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True, label='Email',
                             validators=[EmailValidator()],
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 # 'placeholder':'executeOrder66@gmail.com'
                             }))
    username = forms.CharField(required=True, min_length=3, max_length=15,
                               label='Username',
                               validators=[RegexValidator('^[a-zA-Z0-9_]{3,15}$',
                                                          code='invalid_username',
                                                          message='Username must be more than 3 characters and smaller than 15 with only letters, numbers and underscore.'),
                                           ],
                               widget=forms.TextInput(attrs={
                                   'maxlength': '15',
                                   'class': 'form-control',
                               }),
                               help_text='Username must be more than 3 characters and smaller than 15 with only letters, numbers and underscore.')

    password1 = forms.CharField(required=True, min_length=3, max_length=15,
                                label='Password',
                                validators=[RegexValidator('^[a-zA-Z0-9_]{3,15}$',
                                                           message='Password must be more than 3 characters and smaller than 15 with only letters, numbers and underscore.'),
                                            ],
                                widget=forms.PasswordInput(attrs={
                                    'maxlength': '15',
                                    'class': 'form-control',
                                }),
                                help_text='Password must be more than 3 characters and smaller than 15 with only letters, numbers and underscore.')

    password2 = forms.CharField(required=True, min_length=3, max_length=15,
                                label='Confirm Password',

                                widget=forms.PasswordInput(attrs={
                                    'maxlength': '15',
                                    'class': 'form-control',
                                })
                                )

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password did not match', code='pssword_no_match')

        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError('Email is already taken')

        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError('Username is already taken.')

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(required=True,

                               validators=[RegexValidator('^[a-z0-9_]{3,15}$',
                                                          code='invalid_username',
                                                          message='Invalid Username. You cannot login or register with malformatted username or password'),
                                           ],
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Username'}))

    password = forms.CharField(required=True,
                               validators=[RegexValidator('^[a-zA-Z0-9_]{3,15}$',
                                                          code='invalid_username',
                                                          message='Invalid Password. You cannot login or register with malformatted username or password'),
                                           ],

                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Password'})
                               )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        username = self.cleaned_data.get('username')
        if not User.objects.filter(username__exact=username):
            raise forms.ValidationError('There is no such account.')

        return cleaned_data


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ['name', 'cover_pic', 'description', 'isMarked']
        widgets = {
                'name' :forms.TextInput(attrs={'class': 'form-control mb-3', 'maxlength': '15'}),
                'description': forms.Textarea(attrs={'help_text': 'maxlength is 420',
                                                               'maxlength': '420',
                                                               'rows': "3",
                                                               'class': 'form-control '}),
                'cover_pic': forms.FileInput(),
                'isMarked':forms.CheckboxInput(attrs = { "class": "checkmark",
                                                        })

        }
        labels = {
            'name':'Room Name',
            'description':'Description',
            'cover_pic' :'Room Cover',
            'isMarked' :'Mark Location'
        }
        error_messages = {
            'name': {
                'max_length':"This room name is too long. Maximum is 15 characters",
            },
            'description': {
                'max_length':"This room description is too long. Maximum is 420 characters",
            }
        }
 

    def clean(self):
        cleaned_data = super(RoomForm, self).clean()

        name = self.cleaned_data.get('name')
        if Room.objects.filter(name__exact=name) and not self.instance.name == name:
            raise forms.ValidationError('Room name is already taken.')

        return cleaned_data


class MarkerForm(forms.ModelForm):
  class Meta:
      model = Marker
      fields = ('lat', 'lng')

class ProfileForm(forms.ModelForm):

  class Meta:
    model = Profile
    fields = ['age','bio','img']

    widgets = {
        'age' :forms.NumberInput(attrs = {'class' : 'form-control mr-6' }),
        'bio': forms.Textarea(attrs={'help_text': 'maxlength is 420',
                                                       'maxlength': '420',
                                                       'rows': "8",
                                                       'class': 'form-control '}),
        'img': forms.FileInput()

    }
    labels = {
          'age':'Age',
          'bio':'Description',
          'img' :'Profile Image',
      }
